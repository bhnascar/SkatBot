function y = PredictRankSVM(args)
%PREDICTRANKSVM Predicts the rank of the card that should be played
%   Y = PREDICTRANKSVM(ARGS) is the prediction of the rank that should be
%   played. This function takes in a vector ARGS of features and outputs Y,
%   a single number that indicates which card should be played. x is a 1 x
%   42 array of features.

    load test.mat;
    
    n_features = 42;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    %x = x(2:n_features);
    x(1,1) = 1;
    y_dummy = 1;
    y = svmpredict(y_dummy, x, model_rank, '-q');
end
