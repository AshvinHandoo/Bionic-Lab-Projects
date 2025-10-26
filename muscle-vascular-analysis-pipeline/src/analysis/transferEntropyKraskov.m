% transferEntropyKraskov.m
% Origin: "JIDTkrashkov.m"
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

%% Transfer Entropy (Kraskov, Asymmetry, Random Permutation Null, Multi-Animal)
% - Lag sweep: 0..3 samples
% - K sweep (averaged): [3 4 5 8 10]
% - Random permutation nulls
% - Asymmetry (Ca->Dia, Dia->Ca)
% - Best lag tracking (samples)
% - One CSV per animal

javaaddpath('/Users/ashvinhandoo/Documents/JIDT/infodynamics-dist-1.6.1/infodynamics.jar');

% --- Parameters ---
animals = {'VSF1','VSF2','VSM6','VSM1'};
numVessels = 9;
days = {'d000','d001','d002','d003','d007','d014','d021','d028',...
        'd035','d042','d049','d056','d063','d070','d077','d084'};
k_values = [3 4 5 8 10];
lags = 0:3;                % includes 0-lag case
numSur = 200;              % number of surrogate permutations

% === Loop over each animal ===
for a = 1:length(animals)
    animalName = animals{a};
    fprintf('\n==========================\n');
    fprintf(' Processing Animal: %s\n', animalName);
    fprintf('==========================\n');

    % Initialize storage
    DayCol = {}; VesselCol = [];
    CorrCol = [];
    TE_CaDia = []; TE_DiaCa = [];
    Null_CaDia = []; Null_DiaCa = [];
    Sig_CaDia = []; Sig_DiaCa = [];
    Lag_CaDia = []; Lag_DiaCa = [];

    % --- Loop over days ---
    for i = 1:length(days)
        vesselDay = days{i};
        for j = 1:numVessels
            vesselName = sprintf('Vessel%d', j);
            try
                % --- Load data ---
                Calcium  = VesselStim.(animalName).(vesselDay).(vesselName).Iso.dff0;
                Diameter = VesselStim.(animalName).(vesselDay).(vesselName).Iso.delD_D0;

                % --- Preprocess ---
                Ca = detrend(Calcium(:)); 
                Ca = (Ca - mean(Ca)) ./ std(Ca); 
                Ca = Ca + 1e-8*randn(size(Ca));

                Di = detrend(Diameter(:)); 
                Di = (Di - mean(Di)) ./ std(Di); 
                Di = Di + 1e-8*randn(size(Di));

                corr_coef = corr(Ca, Di);

                % --- Run both directions ---
                [TE1, Null1, Sig1, Lag1] = run_TEsweep(Ca, Di, k_values, lags, numSur);
                [TE2, Null2, Sig2, Lag2] = run_TEsweep(Di, Ca, k_values, lags, numSur);

                % --- Store results ---
                DayCol{end+1,1} = vesselDay;
                VesselCol(end+1,1) = j;
                CorrCol(end+1,1) = corr_coef;
                TE_CaDia(end+1,1) = TE1;
                TE_DiaCa(end+1,1) = TE2;
                Null_CaDia(end+1,1) = Null1;
                Null_DiaCa(end+1,1) = Null2;
                Sig_CaDia(end+1,1) = Sig1;
                Sig_DiaCa(end+1,1) = Sig2;
                Lag_CaDia(end+1,1) = Lag1;
                Lag_DiaCa(end+1,1) = Lag2;

                fprintf('\n%s | %s | %s\n', animalName, vesselDay, vesselName);
                fprintf('r = %.3f | TE(Ca→Dia)=%.4f | TE(Dia→Ca)=%.4f\n', corr_coef, TE1, TE2);
                fprintf('Nulls: [%.4f, %.4f] | Lags: [%d, %d] | Sig: [%d, %d]\n', ...
                        Null1, Null2, Lag1, Lag2, Sig1, Sig2);

            catch
                fprintf('Skipping %s %s %s (missing data)\n', animalName, vesselDay, vesselName);
                continue;
            end
        end
    end

    % --- Build output table ---
    T = table(DayCol, VesselCol, CorrCol, ...
              TE_CaDia, Null_CaDia, Sig_CaDia, Lag_CaDia, ...
              TE_DiaCa, Null_DiaCa, Sig_DiaCa, Lag_DiaCa, ...
              'VariableNames', {'Day','Vessel','PearsonCorr',...
                                'TE_CaToDia','Null_CaToDia','Sig_CaToDia','BestLag_CaToDia',...
                                'TE_DiaToCa','Null_DiaToCa','Sig_DiaToCa','BestLag_DiaToCa'});

    % --- Write CSV per animal ---
    outName = sprintf('Kraskov_%s.csv', animalName);
    writetable(T, outName);
    fprintf('\n✅ CSV exported: %s\n', outName);
end


%% --- Helper Function with Random Permutation Nulls ---
function [TE_avg, Null_avg, isSig, bestLag_global] = run_TEsweep(X, Y, k_values, lags, numSur)
    TE_vals = nan(length(k_values), length(lags));
    Null_vals = nan(length(k_values), 1);
    bestLag_perK = nan(length(k_values),1);

    for kk = 1:length(k_values)
        kset = k_values(kk);
        lagTE = nan(size(lags));

        % ---- Lag sweep ----
        for L = 1:length(lags)
            lag = lags(L);
            if lag == 0
                Xlag = X; Ylag = Y;
            else
                Xlag = X(1:end-lag);
                Ylag = Y(1+lag:end);
            end

            teCalc = javaObject('infodynamics.measures.continuous.kraskov.TransferEntropyCalculatorKraskov');
            teCalc.setProperty('k', num2str(kset));
            teCalc.initialise(1);
            teCalc.setObservations(Xlag, Ylag);
            lagTE(L) = teCalc.computeAverageLocalOfObservations() / log(2);
        end

        % --- Record best lag for this k ---
        [~, idxMax] = max(lagTE);
        bestLag_perK(kk) = lags(idxMax);
        TE_vals(kk,:) = lagTE;

        % --- Random permutation surrogates ---
        bestLag = bestLag_perK(kk);
        if bestLag == 0
            Xlag = X; Ylag = Y;
        else
            Xlag = X(1:end-bestLag);
            Ylag = Y(1+bestLag:end);
        end

        surVals = nan(numSur,1);
        teCalc = javaObject('infodynamics.measures.continuous.kraskov.TransferEntropyCalculatorKraskov');
        teCalc.setProperty('k', num2str(kset));
        teCalc.initialise(1);

        for s = 1:numSur
            Xs = Xlag(randperm(length(Xlag)));  % random permutation null
            teCalc.setObservations(Xs, Ylag);
            surVals(s) = teCalc.computeAverageLocalOfObservations() / log(2);
        end

        Null_vals(kk) = mean(surVals,'omitnan');
    end

    % --- Average across k values ---
    TE_avg = mean(max(TE_vals,[],2,'omitnan'),'omitnan');
    Null_avg = mean(Null_vals,'omitnan');
    bestLag_global = round(mean(bestLag_perK,'omitnan'));

    % --- Significance test ---
    z = (TE_avg - Null_avg) / std(Null_vals);
    isSig = (z > 1.96); % p < 0.05, one-sided
end
