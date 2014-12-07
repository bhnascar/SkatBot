function y = PredictSuitSVM(args)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSVM(ARGS) is the prediction of the suit that should be
%   played. This function takes in a vector ARGS of features and outputs y,
%   a single number between 0 and 3, indicating which suit should be
%   played.

    load svm_parameters.mat;
    
    n_features = 30;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    x = x(2:n_features);
    	
    y1 = svmpredict(1, x, model_suit1, '-q');
    y2 = svmpredict(1, x, model_suit2, '-q');
    y1 = y1-1;
    y2 = y2-1;
    y = [y1 y2];
end

