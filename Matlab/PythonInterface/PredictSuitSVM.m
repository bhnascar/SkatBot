function y = PredictSuitSVM(args)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSVM(ARGS) is the prediction of the suit that should be
%   played. This function takes in a vector ARGS of features and outputs y,
%   a single number between 0 and 3, indicating which suit should be
%   played.

    load softmax_parameters.mat;
    load svm_parameters.mat;
    
    n_features = 30;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end
    
    % Softmax
    x(1,1) = 1;     
    p = exp(theta_suit'*(x'));
    p = p./sum(exp(theta_suit'*(x')));
    [~, y] = sort(p, 'descend');
    y4 = y;
    
    % SVM
    x = x(2:n_features);    	
    y1 = svmpredict(1, x, model_suit1, '-q');
    y2 = svmpredict(1, x, model_suit2, '-q');
    y3 = svmpredict(1, x, model_suit3, '-q');
    
    y = y4 - 1;
end

