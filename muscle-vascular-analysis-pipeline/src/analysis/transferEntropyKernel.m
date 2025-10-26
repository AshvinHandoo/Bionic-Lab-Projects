% transferEntropyKernel.m
% Origin: "JIDTkernel.m"
% Category: Analytical routines (Transfer Entropy, meta-analysis)
% Author: Ashvin Handoo
% Last Updated: 2025-10-26
%
% Summary:
%   Part of the astrocyte-vascular-analysis-pipeline. Renamed and documented
%   for clarity and recruiter readability. Original logic preserved.
%
% Notes:
%   - See README for a synthetic demo you can run without lab data.
%   - This file may expect specific data structures if used with raw datasets.
%
% ---- Original script content below ----

%% Transfer Entropy (Kernel Estimator, Asymmetry, Random Permutation Null, Multi-Animal)
% Mirrors the Kraskov pipeline but uses JIDT's kernel estimator.
% - Lag sweep: 0..3 samples
% - Bandwidth sweep (averaged): [0.5 0.7 1.0 1.3 1.6]
% - Random permutation nulls
% - Asymmetry (Ca->Dia, Dia->Ca)
% - Best lag tracking (samples)
% - One CSV per animal

javaaddpath('/Users/ashvinhandoo/Documents/JIDT/infodynamics-dist-1.6.1/infodynamics.jar');

% ---------- Parameters ----------
animals = {'VSF1','VSF2','VSM6','VSM1'};
numVessels = 9;
days = {'d000','d001','d002','d003','d007','d014','d021','d028',...
        'd035','d042','d049','d056','d063','d070','d077','d084'};

% Kernel estimator bandwidths (in SD units since NORMALISE=true)
bw_values = [0.5 0.7 1.0 1.3 1.6];

% Lags (in samples) to test; includes 0-lag
lags = 0:3;

% Number of random permutation surrogates
numSur = 200;

% Add a tiny jitter after z-scoring to avoid kernel/neighbor ties
EPS = 1e-8;

% ---------- Loop over animals ----------
for a = 1:length(animals)
    animalName = animals{a};
    fprintf('\n==========================\n');
    fprintf(' Processing Animal: %s (Kernel Estimator)\n', animalName);
    fprintf('==========================\n');

    % Storage for this animal
    DayCol = {}; VesselCol = [];
    CorrCol = [];
    TE_CaDia = []; TE_DiaCa = [];
    Null_CaDia = []; Null_DiaCa = [];
    Sig_CaDia = []; Sig_DiaCa = [];
    Lag_CaDia = []; Lag_DiaCa = [];

    % ---------- Iterate days/vessels ----------
    for i = 1:length(days)
        vesselDay = days{i};

        for j = 1:numVessels
            vesselName = sprintf('Vessel%d', j);
            try
                % ---- Load real data ----
                Calcium  = VesselStim.(animalName).(vesselDay).(vesselName).Iso.dff0;
                Diameter = VesselStim.(animalName).(vesselDay).(vesselName).Iso.delD_D0;

                Calcium  = Calcium(:);
                Diameter = Diameter(:);

                % ---- Preprocess: detrend, z-score, tiny jitter ----
                Ca = detrend(Calcium); Ca = (Ca - mean(Ca))./std(Ca); Ca = Ca + EPS*randn(size(Ca));
                Di = detrend(Diameter); Di = (Di - mean(Di))./std(Di); Di = Di + EPS*randn(size(Di));

                % Basic linear correlation for reference
                corr_coef = corr(Ca, Di);

                % ---- Run both directions with kernel estimator ----
                [TE1, Null1, Sig1, Lag1] = run_TEsweep_kernel(Ca, Di, bw_values, lags, numSur);
                [TE2, Null2, Sig2, Lag2] = run_TEsweep_kernel(Di, Ca, bw_values, lags, numSur);

                % ---- Store row ----
                DayCol{end+1,1} = vesselDay;
                VesselCol(end+1,1) = j;
                CorrCol(end+1,1) = corr_coef;

                TE_CaDia(end+1,1)   = TE1;
                Null_CaDia(end+1,1) = Null1;
                Sig_CaDia(end+1,1)  = Sig1;
                Lag_CaDia(end+1,1)  = Lag1;

                TE_DiaCa(end+1,1)   = TE2;
                Null_DiaCa(end+1,1) = Null2;
                Sig_DiaCa(end+1,1)  = Sig2;
                Lag_DiaCa(end+1,1)  = Lag2;

                % ---- Console log ----
                fprintf('\n%s | %s | %s\n', animalName, vesselDay, vesselName);
                fprintf('r = %.3f | TE(Ca→Dia)=%.4f | TE(Dia→Ca)=%.4f\n', corr_coef, TE1, TE2);
                fprintf('Nulls: [%.4f, %.4f] | Best Lags: [%d, %d] | Sig: [%d, %d]\n', ...
                        Null1, Null2, Lag1, Lag2, Sig1, Sig2);

            catch
                fprintf('Skipping %s %s %s (missing data)\n', animalName, vesselDay, vesselName);
                continue;
            end
        end
    end

    % ---- Build output table & CSV per animal ----
    T = table(DayCol, VesselCol, CorrCol, ...
              TE_CaDia, Null_CaDia, Sig_CaDia, Lag_CaDia, ...
              TE_DiaCa, Null_DiaCa, Sig_DiaCa, Lag_DiaCa, ...
              'VariableNames', {'Day','Vessel','PearsonCorr',...
                                'TE_CaToDia','Null_CaToDia','Sig_CaToDia','BestLag_CaToDia',...
                                'TE_DiaToCa','Null_DiaToCa','Sig_DiaToCa','BestLag_DiaToCa'});

    outName = sprintf('Kernel_%s.csv', animalName);
    writetable(T, outName);
    fprintf('\n✅ CSV exported: %s\n', outName);
end


% ===================== Helper: Kernel TE with lag + bandwidth sweeps =====================
function [TE_avg, Null_avg, isSig, bestLag_global] = run_TEsweep_kernel(X, Y, bw_values, lags, numSur)
    numBW = numel(bw_values);
    TE_best_perBW   = nan(numBW,1);
    Null_mean_perBW = nan(numBW,1);
    bestLag_perBW   = nan(numBW,1);

    for bb = 1:numBW
        bw = bw_values(bb);

        % ---- Lag sweep for this bandwidth ----
        lagTE = nan(numel(lags),1);
        for L = 1:numel(lags)
            lag = lags(L);
            if lag == 0
                Xlag = X; Ylag = Y;
            else
                Xlag = X(1:end-lag);
                Ylag = Y(1+lag:end);
            end

            teCalc = javaObject('infodynamics.measures.continuous.kernel.TransferEntropyCalculatorKernel');
            teCalc.setProperty('NORMALISE', 'true');      
            teCalc.setProperty('KERNEL_WIDTH', num2str(bw));
            teCalc.initialise(1);
            teCalc.setObservations(Xlag, Ylag);
            lagTE(L) = teCalc.computeAverageLocalOfObservations() / log(2);
        end

        % ---- pick the best lag for this bandwidth ----
        [TEbest, idxMax] = max(lagTE, [], 'omitnan');
        bestLag = lags(idxMax);
        TE_best_perBW(bb) = TEbest;
        bestLag_perBW(bb) = bestLag;

        % ---- random permutation surrogates at that best lag ----
        if bestLag == 0
            Xlag = X; Ylag = Y;
        else
            Xlag = X(1:end-bestLag);
            Ylag = Y(1+bestLag:end);
        end

        surVals = nan(numSur,1);
        teCalc = javaObject('infodynamics.measures.continuous.kernel.TransferEntropyCalculatorKernel');
        teCalc.setProperty('NORMALISE', 'true');
        teCalc.setProperty('KERNEL_WIDTH', num2str(bw));
        teCalc.initialise(1);

        for s = 1:numSur
            Xs = Xlag(randperm(length(Xlag))); % random permutation
            teCalc.setObservations(Xs, Ylag);
            surVals(s) = teCalc.computeAverageLocalOfObservations() / log(2);
        end

        Null_mean_perBW(bb) = mean(surVals, 'omitnan');
    end

    % ---- Aggregate across bandwidths ----
    TE_avg         = mean(TE_best_perBW, 'omitnan');
    Null_avg       = mean(Null_mean_perBW, 'omitnan');
    bestLag_global = round(mean(bestLag_perBW, 'omitnan'));

    % ---- Significance test ----
    z = (TE_avg - Null_avg) / std(Null_mean_perBW, 0, 'omitnan');
    isSig = (z > 1.96);   
end