function y = PredictRankSVM(args)
%PREDICTRANKSVM Predicts the rank of the card that should be played
%   Y = PREDICTRANKSVM(ARGS) is the prediction of the rank that should be
%   played. This function takes in a vector ARGS of features and outputs Y,
%   a single number that indicates which card should be played. x is a 1 x
%   42 array of features.

    load svm_parameters.mat;
    
    n_features = 42;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    x = x(2:n_features);
    
    y1 = svmpredict(1, x, model_rank1, '-q');
    y2 = svmpredict(1, x, model_rank2, '-q');
    y1 = y1-1;
    y2 = y2-1;
    y = [y1 y2];
end
