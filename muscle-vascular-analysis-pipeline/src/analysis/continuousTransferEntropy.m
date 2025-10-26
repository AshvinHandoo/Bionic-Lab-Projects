% continuousTransferEntropy.m
% Origin: "JIDTcont.m"
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

%% Java Information Dynamics Toolkit (JIDT)
%% Continuous Transfer Entropy using Kernel Estimators on real calcium and diameter data
%%

% Add JIDT jar path
javaaddpath('/Users/ashvinhandoo/Documents/JIDT/infodynamics-dist-1.6.1/infodynamics.jar');

% Define vessels and days
numVessels = 9;
numDays = length(days);
numObservations = 587;
days = {'d000', 'd001', 'd002', 'd003', 'd007', 'd014', 'd021', 'd028', 'd035', 'd042', 'd049', 'd056', 'd063', 'd070', 'd077', 'd084'};


% Define variables
DayCol        = {};
VesselCol     = [];
CorrCol       = [];
TECol         = [];
RandTECol     = [];
NullMeanCol   = [];
NullStdCol    = [];
SignificanceCol = [];

for i = 1:numDays
    vesselDay = days{i};

    for j = 1:numVessels
        vesselName = sprintf('Vessel%d', j);
        try
            % Load calcium and diameter data
            Calcium  = VesselStim.VSM6.(vesselDay).(vesselName).Iso.dff0;
            Diameter = VesselStim.VSM6.(vesselDay).(vesselName).Iso.delD_D0;

            Calcium  = Calcium(:);
            Diameter = Diameter(:);

            % Pearson correlation
            corr_coef = corr(Calcium, Diameter);

            % Random signal0
            Random = Calcium(randperm(length(Calcium)));

            % Set up TE calculator
            teCalc = javaObject('infodynamics.measures.continuous.kernel.TransferEntropyCalculatorKernel');
            teCalc.setProperty('NORMALISE', 'true');
            teCalc.initialise(2, 1);
            teCalc.setObservations(Calcium, Diameter);

            result = teCalc.computeAverageLocalOfObservations();

            % Random TE
            teCalc.initialise();
            teCalc.setObservations(Random, Diameter);
            result2 = teCalc.computeAverageLocalOfObservations();

            % Null distribution
            nullDist = teCalc.computeSignificance(100);
            nullMean = nullDist.getMeanOfDistribution();
            nullStd  = nullDist.getStdOfDistribution();

            % Significance check
            isSignificant = nullStd * 1.96 + nullMean < result;

            DayCol{end+1,1}      = vesselDay;
            VesselCol(end+1,1)   = j;
            CorrCol(end+1,1)     = corr_coef;
            TECol(end+1,1)       = result;
            RandTECol(end+1,1)   = result2;
            NullMeanCol(end+1,1) = nullMean;
            NullStdCol(end+1,1)  = nullStd;
            SignificanceCol(end+1,1) = isSignificant;

            % Print results
            fprintf('\n=== Results for %s %s ===\n', vesselDay, vesselName);
            fprintf('Pearson correlation coefficient: %.4f\n', corr_coef);
            fprintf('Transfer Entropy (Calcium -> Diameter): %.4f bits\n', result);
            fprintf('Transfer Entropy (Random -> Diameter): %.4f bits\n', result2);
            fprintf('Null mean: %.4f, std: %.4f\n', nullMean, nullStd);
            if isSignificant
                fprintf('Result is SIGNIFICANT.\n');
            else
                fprintf('Result is NOT significant.\n');
            end

        catch
            fprintf('Skipping %s %s (not found).\n', vesselDay, vesselName);
            continue;
        end
    end
end

% Create table
T = table(DayCol, VesselCol, CorrCol, TECol, RandTECol, NullMeanCol, NullStdCol, SignificanceCol, ...
    'VariableNames', {'Day', 'Vessel', 'PearsonCorr', 'TE_Ca_Dia', 'TE_Rand_Dia', 'NullMean', 'NullStd', 'Significance'});

% Write to CSV
writetable(T, 'VSM6resultsnew.csv');
fprintf("\n CSV exported \n");

%Pearson correlation refers to the linear correlation between the 2 signals 
%Negative means that as the calcium increases diameter decreases (makes
%sense calcium means that the vessel is contracting
%Transfer entropy values refers to how much knowing calcium reduces uncertainty about future diameter
%Null distribution mean refers to the overall significance

%1 bit of information reduces uncertainty by a factor of 2 (because log₂(2) = 1)
%It means that knowing the source (here, Random signal) reduces uncertainty in predicting the destination (Diameter) by 0.0607 bits per sample

%subplot(2,1,1)
%plot(VesselStim.VSM6.d070.Vessel1.Iso.dff0)

%subplot(2,1,2)
%plot(VesselStim.VSM6.d070.Vessel1.Iso.delD_D0)

%Notes for d000
%Increase of calcium decreases vessel (Very negative coefficient)
%Small but statistically signifcant TE

      %1        -0.85347      0.015436      0.0020158      0.0012135    0.0024208
      %2         -0.6537      0.030854     -0.0036695      0.0018645    0.0036072
      %3        -0.57757      0.022649       -0.00188      0.0027525     0.003414
      %4        -0.71239      0.023423     -0.0041205     0.00098525    0.0031404
      %5        -0.67073      0.020794      0.0007251       0.001457    0.0030541
      %6        -0.72812      0.038296      0.0019342     0.00086425    0.0026408

%Notes for d070 (some issue on 84)
%Still same coefficent
%Still some small signifcant TE
%TE is overall smaller

      %1         -0.7332         0.014361     0.00041232     6.084e-05    0.0018438
      %2        -0.68624         0.011309    -0.00057917    0.00031864    0.0017608
      %3        -0.51456         0.018013      0.0017213     0.0010005    0.0024991
      %4        -0.38222        0.0024494      -0.001562    0.00062354    0.0020793
      %5        -0.25982      -0.00063982    -0.00041934     0.0020447    0.0039298
      %6        -0.58257         0.010261      0.0003545    0.00076176    0.0021117