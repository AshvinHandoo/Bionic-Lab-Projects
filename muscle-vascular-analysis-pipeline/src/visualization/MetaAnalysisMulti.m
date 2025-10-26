% MetaAnalysisMulti.m
% -------------------------------------------------------------------------
% Purpose:
%   Aggregates and visualizes transfer entropy (TE) results across multiple
%   animals or vessels. Produces averaged TE plots to show group-level
%   patterns and coupling consistency.
%
% Inputs:
%   - CSV files from multiple animals or vessels (TE outputs)
%
% Outputs:
%   - Averaged plots and summary figures across datasets
%
% File Relationships:
%   - Builds on outputs from TransferEntropyKraskov and TransferEntropyKernel
%   - Provides intermediate visualizations used before
%     PlotVascularCorrelation
%
% Dependencies:
%   - MATLAB plotting functions
%
% ---- Original script content below ----

% Basic analysis on results (calculates average TE of all animals separated by vessel)

days = [0, 1, 2, 3, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84];
numDays = length(days);
numVessels = 9;

shortenedVSF1 = VSF1resultskraskov(ismember(VSF1resultskraskov.Day, days), :);
shortenedVSF2 = VSF2resultskraskov(ismember(VSF2resultskraskov.Day, days), :);
shortenedVSM1 = VSM1resultskraskov(ismember(VSM1resultskraskov.Day, days), :);
shortenedVSM6 = VSM6resultskraskov(ismember(VSM6resultskraskov.Day, days), :);

datasets = {shortenedVSF1, shortenedVSF2, shortenedVSM1, shortenedVSM6};

% Initialize storage: [days x vessels x animals]
allData = NaN(numDays, numVessels, numel(datasets));

for d = 1:numel(datasets)
    Data = datasets{d};
    
    for dayIdx = 1:numDays
        dayVal = days(dayIdx);
        
        for v = 1:numVessels
            rows = Data(Data.Day == dayVal & Data.Vessel == v, :);
            
            if ~isempty(rows)
                allData(dayIdx, v, d) = mean(rows.RandTE_meanSweep, 'omitnan');
            end
        end
    end
end

meanAcrossAnimals = mean(allData, 3, 'omitnan');
stdAcrossAnimals = std(allData, 0, 3, 'omitnan');

% Plotting
yLimits   = [-0.04 0.04];
yTickStep = 0.01;

figure;
numRows = ceil(sqrt(numVessels));
numCols = ceil(numVessels / numRows);

for v = 1:numVessels
    y = meanAcrossAnimals(:, v);
    y_std = stdAcrossAnimals(:, v);
    
    if all(isnan(y))
        continue
    end
    
    subplot(numRows, numCols, v);
    errorbar(days, y, y_std, '-o', 'LineWidth', 1.2);
    xlabel('Day');
    ylabel('Mean TE');
    title(sprintf('Vessel %d', v));
    grid on;

    ylim(yLimits);
    yticks(yLimits(1):yTickStep:yLimits(2));
end

sgtitle('Mean TE over Days for Each Vessel (rand)');
