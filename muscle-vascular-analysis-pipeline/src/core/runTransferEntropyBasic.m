% runTransferEntropy.m
% Origin: "JIDT.m"
% Category: Core wrappers / orchestration
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

%% JIDT Transfer Entropy Analysis Script (Final Corrected)

% Add JIDT jar path - run this ONCE per session
javaaddpath('/Users/ashvinhandoo/Documents/JIDT/infodynamics-dist-1.6.1/infodynamics.jar');

%% Load your data
% Replace these with your actual data loading lines
Calcium = VesselStim.VSF1.d000.Vessel1.HundredHz.dff0; % [391 x 1]
Diameter = VesselStim.VSF1.d000.Vessel1.HundredHz.delD_D0; % [1 x 391]

%% Ensure both are column vectors with matching length
Calcium = Calcium(:); % force column
Diameter = Diameter(:); % force column

% Check they have the same length
if length(Calcium) ~= length(Diameter)
    error('Calcium and Diameter must have the same number of data points.');
end

%% Generate control data: random binary array of same length
Random = (rand(length(Diameter),1) > 0.5) * 1;

%% Discretization parameters
numBins = 3; % adjust based on data distribution and sample size

% Create bin edges (add eps to max to include maximum value in last bin)
bin_edges_calcium = linspace(min(Calcium), max(Calcium)+eps, numBins+1);
bin_edges_diameter = linspace(min(Diameter), max(Diameter)+eps, numBins+1);

%% Discretize data into bins
Calcium_discrete = discretize(Calcium, bin_edges_calcium);
Diameter_discrete = discretize(Diameter, bin_edges_diameter);

% Check for NaNs in discretization (should not happen if edges are correct)
if any(isnan(Calcium_discrete))
    error('Calcium discretization produced NaNs – adjust bin edges.');
end
if any(isnan(Diameter_discrete))
    error('Diameter discretization produced NaNs – adjust bin edges.');
end

% Force indices within valid range (1:numBins)
Calcium_discrete(Calcium_discrete > numBins) = numBins;
Diameter_discrete(Diameter_discrete > numBins) = numBins;

% Convert from MATLAB (1:numBins) to JIDT (0:numBins-1) indexing
Calcium_discrete = int32(Calcium_discrete(:) - 1);
Diameter_discrete = int32(Diameter_discrete(:) - 1);
Random = int32(Random(:)); % already binary, convert to int32

%% Initialize Transfer Entropy calculator (Discrete)
% Base = numBins, history length = 1
teCalc = javaObject('infodynamics.measures.discrete.TransferEntropyCalculatorDiscrete', numBins, 1);
teCalc.initialise();

%% Calculate TE from Calcium to Diameter
teCalc.addObservations(Calcium_discrete, Diameter_discrete);
result = teCalc.computeAverageLocalOfObservations();
fprintf('Transfer Entropy (Calcium -> Diameter): %.4f\n', result);

%% Reset calculator before new calculation
teCalc.initialise();

%% Calculate TE from Random to Diameter as control
teCalc.addObservations(Random, Diameter_discrete);
result2 = teCalc.computeAverageLocalOfObservations();
fprintf('Transfer Entropy (Random -> Diameter): %.4f\n', result2);
