% metaAnalysisSingle.m
% Origin: "JIDTmeta_analysis_single.m"
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

%Basic analysis on results (calculates average TE of a single animal)

days = [0, 1, 2, 3, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84];

shortenedResultsVSF1 = VSF1resultskraskov(ismember(VSF1resultskraskov.Day, days), :);

[i, dayNames] = findgroups(shortenedResultsVSF1.Day);
meanTEVSF1 = splitapply(@mean, shortenedResultsVSF1.TE_Rand_Dia, i);

stdTEVSF1 = splitapply(@std, shortenedResultsVSF1.TE_Rand_Dia, i);

figure;
errorbar(dayNames, meanTEVSF1, stdTEVSF1, '-o');
yLimits = [-0.1 0.1];
ylim(yLimits);
xlabel('Day');
ylabel('Mean TE across vessels');
title('TE for VSF1 after averaging all vessels together (rand)');
