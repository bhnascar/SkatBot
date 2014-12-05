function y = PredictSuitSVM(args)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSVM(ARGS) is the prediction of the suit that should be
%   played. This function takes in a vector ARGS of features and outputs y,
%   a single number between 0 and 3, indicating which suit should be
%   played.

    load test.mat;
    
    n_features = 30;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    %x = x(2:n_features);
    x(1,1) = 1;
	
    y_dummy = 1;
    y = svmpredict(y_dummy, x, model_suit, '-q');
end

