function [y] = PredictRankSVM(args)
%PREDICTRANKSVM Predicts the rank of the card that should be played
%   Y = PREDICTRANKSVM(X) is the prediction of the rank that should be
%   played. This function takes in a vector X of features and outputs Y,
%   a single number that indicates which card should be played. x is a 1 x
%   42 array of features.

    Initialize();
    fields = fieldnames(args);
    x = zeros(1, 42);
    for i = 1:numel(fields)
        x(i) = args.(fields{i});
    end            
    x = x(2:42);
    y_dummy = 1;
    y = svmpredict(y_dummy, x, model_rank, '-q');
end
