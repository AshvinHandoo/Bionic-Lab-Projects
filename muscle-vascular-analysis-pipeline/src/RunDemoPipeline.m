% RunDemoPipeline.m
% -------------------------------------------------------------------------
% Purpose:
%   Demonstrates the astrocyte-vascular-analysis-pipeline workflow using
%   synthetic data. Runs the generator, computes rolling correlations, and
%   produces a simple summary and plot.
%
% Inputs:
%   - None (synthetic data generated automatically)
%
% Outputs:
%   - CSV summary and PNG plot in the results directory
%
% File Relationships:
%   - Calls GenerateSyntheticVascularData.m for demo data
%   - Independent from experimental scripts
%
% Dependencies:
%   - MATLAB base environment
%
% -------------------------------------------------------------------------

function runDemoPipeline()
% runDemoPipeline
% End-to-end demo for astrocyte-vascular-analysis-pipeline using synthetic data.
%
% Steps:
%   1) Generate synthetic vasomotion + calcium
%   2) Compute a rolling correlation as a simple coupling proxy
%   3) Save a summary and a plot under results/
%
root = fileparts(fileparts(mfilename('fullpath')));
resDir = fullfile(root, 'results');
plotDir = fullfile(resDir, 'generated_plots');
if ~exist(plotDir,'dir'); mkdir(plotDir); end
% 1) Generate synthetic data
csvPath = generateSyntheticVascularData();
T = readtable(csvPath);
% 2) Rolling correlation (window 101 ~ 10s at 10 Hz)
w = 101;
rc = rollingCorr(T.vasomotion, T.calcium, w);
T.rolling_corr = rc;
% 3) Save summary
outCSV = fullfile(resDir, 'vascular_output_summary.csv');
writetable(T, outCSV);
% 4) Plot
f = figure('Visible','off'); %#ok<UNRCH>
yyaxis left
plot(T.time, T.vasomotion, 'DisplayName','Vasomotion'); hold on;
plot(T.time, T.calcium, 'DisplayName','Calcium');
xlabel('Time (s)'); ylabel('Signal');
legend('Location','best');
yyaxis right
plot(T.time, T.rolling_corr, 'DisplayName','Rolling Corr');
ylabel('Rolling Corr');
title('Synthetic Vasomotion & Calcium with Rolling Correlation');
outPNG = fullfile(plotDir, 'synthetic_vascular_corr.png');
saveas(f, outPNG);
close(f);
fprintf('Summary saved to: %s\n', outCSV);
fprintf('Plot saved to: %s\n', outPNG);
end
function rc = rollingCorr(x, y, w)
    n = numel(x);
    rc = nan(n,1);
    half = floor(w/2);
    for i=1:n
        s = max(1, i-half);
        e = min(n, i+half);
        xi = x(s:e); yi = y(s:e);
        if numel(xi) > 2
            c = corrcoef(xi, yi);
            rc(i) = c(1,2);
        end
    end
end
