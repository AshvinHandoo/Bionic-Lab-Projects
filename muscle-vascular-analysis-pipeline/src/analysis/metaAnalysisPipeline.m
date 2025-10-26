% metaAnalysisPipeline.m
% Origin: "JIDTmeta_analysis.m"
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

%Basic analysis on results

%Iso for VSF1

[i, dayNames] = findgroups(results3.Day);
meanTE = splitapply(@mean, results3.TE_Ca_Dia, i);
disp(meanTE)

plot(meanTE)

%Day 77 and 84 not signifcant 

%Iso for VSF2
