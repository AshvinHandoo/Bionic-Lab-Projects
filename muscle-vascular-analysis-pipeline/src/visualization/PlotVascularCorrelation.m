% PlotVascularCorrelation.m
% -------------------------------------------------------------------------
% Purpose:
%   Generates comprehensive visualizations combining all animals, vessels,
%   and days. Displays directional coupling (calcium → diameter and
%   diameter → calcium) along with null distributions and averaged results.
%
% Inputs:
%   - CSV outputs from TransferEntropyKraskov or TransferEntropyKernel
%     across all animals
%
% Outputs:
%   - Figures summarizing group-level TE patterns and null comparisons
%
% File Relationships:
%   - Extends MetaAnalysisSingle and MetaAnalysisMulti
%   - Final visualization stage in the analysis pipeline
%
% Dependencies:
%   - MATLAB plotting functions
%
% ---- Original script content below ----

%% ==========================================================
%  MASTER TE GRAPHING PROGRAM (with lag mode + significance %)
%  Plots summary figures for both directions (Ca→Dia, Dia→Ca)
%  and for both true TE and Null TE (random baseline).
%  Shows average best lag, most common lag (with %), and %
%  significant datapoints in each title.
%
%  Expected data variables in workspace:
%  VSF1results, VSF2results, VSM1results, VSM6results
% ===========================================================

days = [0, 1, 2, 3, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84];
numDays = length(days);
numVessels = 9;

datasets = {KernelVSF1, KernelVSF2, KernelVSM1, KernelVSM6};
animalNames = {'VSF1','VSF2','VSM1','VSM6'};

% === PARAMETERS FOR PLOTTING ===
yLimits   = [-0.5 0.5];
yTickStep = 0.1;

% === TYPES OF ANALYSES ===
directions = {'CaToDia','DiaToCa'};
types = {'TE','Null'};

% Loop over directions and TE types
for d = 1:numel(directions)
    dirName = directions{d};

    for t = 1:numel(types)
        typeName = types{t};

        % Column names depend on direction/type
        valueCol = sprintf('%s_%s', typeName, dirName);      % e.g. TE_CaToDia
        lagCol   = sprintf('BestLag_%s', dirName);           % e.g. BestLag_CaToDia
        sigCol   = sprintf('Sig_%s', dirName);               % e.g. Sig_CaToDia

        %% -------------------------------
        % 1️⃣  Individual Animal – Averaged Across Vessels
        % -------------------------------
        for a = 1:numel(animalNames)
            tbl = datasets{a};
            name = animalNames{a};
            shortTbl = tbl(ismember(tbl.Day, days), :);

            [grp, dayNames] = findgroups(shortTbl.Day);
            meanVals = splitapply(@mean, shortTbl.(valueCol), grp);
            stdVals  = splitapply(@std,  shortTbl.(valueCol), grp);

            % Compute lag + significance stats for this animal subset
            [modeLag, modePct] = modeWithPercent(shortTbl.(lagCol));
            meanLag  = mean(shortTbl.(lagCol), 'omitnan');
            sigPct   = 100 * mean(shortTbl.(sigCol), 'omitnan');

            figure;
            errorbar(dayNames, meanVals, stdVals, '-o', 'LineWidth', 1.2);
            ylim(yLimits); yticks(yLimits(1):yTickStep:yLimits(2));
            xlabel('Day'); ylabel('Mean TE across vessels');
            title(sprintf('%s %s (%s)\nMean lag=%.1f | Mode lag=%d (%.0f%%) | Sig=%.0f%%', ...
                  name, typeName, directionLabel(dirName), meanLag, modeLag, modePct, sigPct));
            grid on;
        end

        %% -------------------------------
        % 2️⃣  All Animals – Separated by Vessel
        % -------------------------------
        allData = NaN(numDays, numVessels, numel(datasets));
        allLags = NaN(numDays, numVessels, numel(datasets));
        allSigs = NaN(numDays, numVessels, numel(datasets));

        for a = 1:numel(datasets)
            Data = datasets{a};
            for dayIdx = 1:numDays
                dayVal = days(dayIdx);
                for v = 1:numVessels
                    rows = Data(Data.Day == dayVal & Data.Vessel == v, :);
                    if ~isempty(rows)
                        allData(dayIdx,v,a) = mean(rows.(valueCol), 'omitnan');
                        allLags(dayIdx,v,a) = mean(rows.(lagCol), 'omitnan');
                        allSigs(dayIdx,v,a) = mean(rows.(sigCol), 'omitnan');
                    end
                end
            end
        end

        meanAcrossAnimals = mean(allData, 3, 'omitnan');
        stdAcrossAnimals  = std(allData, 0, 3, 'omitnan');

        % Lag + sig stats across all data points
        allLagsFlat = allLags(:);
        allSigsFlat = allSigs(:);
        [modeLag, modePct] = modeWithPercent(allLagsFlat);
        meanLagOverall = mean(allLagsFlat, 'omitnan');
        sigPctOverall = 100 * mean(allSigsFlat, 'omitnan');

        figure;
        numRows = ceil(sqrt(numVessels));
        numCols = ceil(numVessels / numRows);

        for v = 1:numVessels
            y = meanAcrossAnimals(:, v);
            y_std = stdAcrossAnimals(:, v);
            if all(isnan(y)), continue; end

            subplot(numRows, numCols, v);
            errorbar(days, y, y_std, '-o', 'LineWidth', 1.1);
            xlabel('Day'); ylabel('Mean TE');
            title(sprintf('Vessel %d', v));
            ylim(yLimits); yticks(yLimits(1):yTickStep:yLimits(2));
            grid on;
        end

        sgtitle(sprintf('Mean %s (%s)\nMean lag=%.1f | Mode lag=%d (%.0f%%) | Sig=%.0f%%', ...
                 typeName, directionLabel(dirName), meanLagOverall, modeLag, modePct, sigPctOverall));

        %% -------------------------------
        % 3️⃣  All Animals – Averaged Across Vessels
        % -------------------------------
        allMeanMatrix = NaN(length(days), numel(datasets));

        for a = 1:numel(datasets)
            tbl = datasets{a};
            shortTbl = tbl(ismember(tbl.Day, days), :);
            allMeanMatrix(:,a) = arrayfun(@(dVal) ...
                mean(shortTbl.(valueCol)(shortTbl.Day==dVal), 'omitnan'), days);
        end

        meanTE = mean(allMeanMatrix, 2, 'omitnan');
        stdTE  = std(allMeanMatrix, 0, 2, 'omitnan');

        % Lag + sig stats overall
        combinedTbl = vertcat(datasets{:});
        [modeLag, modePct] = modeWithPercent(combinedTbl.(lagCol));
        meanLagOverall = mean(combinedTbl.(lagCol), 'omitnan');
        sigPctOverall  = 100 * mean(combinedTbl.(sigCol), 'omitnan');

        figure;
        errorbar(days, meanTE, stdTE, '-o', 'LineWidth', 1.3);
        xlabel('Day'); ylabel('Mean TE across animals and vessels');
        ylim(yLimits); yticks(yLimits(1):yTickStep:yLimits(2));
        grid on;
        title(sprintf('Average %s (%s)\nMean lag=%.1f | Mode lag=%d (%.0f%%) | Sig=%.0f%%', ...
              typeName, directionLabel(dirName), meanLagOverall, modeLag, modePct, sigPctOverall));

        % Print quick summary
        fprintf('\nSummary: %s (%s)\nMean lag = %.2f | Mode lag = %d (%.0f%%) | Sig = %.1f%%\n', ...
                typeName, dirName, meanLagOverall, modeLag, modePct, sigPctOverall);
    end
end

%% ==========================================================
% Helper for human-readable direction titles
% ==========================================================
function label = directionLabel(dirName)
    switch dirName
        case 'CaToDia'
            label = 'Calcium → Diameter';
        case 'DiaToCa'
            label = 'Diameter → Calcium';
        otherwise
            label = dirName;
    end
end

%% ==========================================================
% Helper to compute mode lag and percentage
% ==========================================================
function [mVal, pct] = modeWithPercent(data)
    data = data(~isnan(data));
    if isempty(data)
        mVal = NaN; pct = 0;
        return
    end
    mVal = mode(round(data));  % round in case of non-integer lags
    pct  = 100 * sum(round(data) == mVal) / numel(data);
end
