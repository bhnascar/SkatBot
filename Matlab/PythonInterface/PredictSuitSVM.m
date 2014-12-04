function [y] = PredictSuitSVM(x)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSVM(X) is the prediction of the suit that should be
%   played. This function takes in a vector x of features and outputs y,
%   a single number between 1 and 4, indicating which suit should be
%   played.

load svm.mat;
y_dummy = 1;
y = svmpredict(y_dummy, x, model_suit, '-q');


end

