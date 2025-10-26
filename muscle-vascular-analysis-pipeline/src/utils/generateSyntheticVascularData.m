function outPath = generateSyntheticVascularData(seed, n, fs, outDir)
% generateSyntheticVascularData
% Create synthetic vasomotion and calcium signals for demo purposes.
%
% Outputs a .mat and .csv under results/synthetic_data/
%   - time, vasomotion, calcium
%
% Usage:
%   outPath = generateSyntheticVascularData();  % defaults
%
if nargin < 1 || isempty(seed), seed = 42; end
if nargin < 2 || isempty(n),    n = 3000;   end
if nargin < 3 || isempty(fs),   fs = 10.0;  end
if nargin < 4 || isempty(outDir)
    outDir = fullfile(fileparts(fileparts(fileparts(mfilename('fullpath')))), 'results', 'synthetic_data');
end
if exist('rng','file')
    rng(seed);
end
t = (0:n-1)'/fs;
% Slow vasomotion (~0.1 Hz) + noise
vasomotion = 0.8*sin(2*pi*0.1*t) + 0.2*sin(2*pi*0.03*t + 0.7) + 0.15*randn(n,1);
% Calcium with partial coupling to vasomotion
calcium = 0.6*sin(2*pi*0.12*t + 0.4) + 0.25*sin(2*pi*0.03*t - 0.5) + 0.18*randn(n,1);
% Inject segments of higher coupling
segments = [500 850; 1500 1800; 2300 2600];
for k = 1:size(segments,1)
    s = segments(k,1); e = min(segments(k,2), n);
    calcium(s:e) = 0.65*vasomotion(s:e) + 0.2*randn(e-s+1,1);
end
T = table(t, vasomotion, calcium, 'VariableNames', {'time','vasomotion','calcium'});
if ~exist(outDir, 'dir'); mkdir(outDir); end
matPath = fullfile(outDir, 'vascular_signals.mat');
csvPath = fullfile(outDir, 'vascular_signals.csv');
save(matPath, 'T');
% Write CSV (basic)
fid = fopen(csvPath, 'w');
fprintf(fid, 'time,vasomotion,calcium\n');
fclose(fid);
dlmwrite(csvPath, T{:,:}, '-append');
if nargout > 0
    outPath = csvPath;
end
fprintf('Synthetic data written to: %s\n', outDir);
end
