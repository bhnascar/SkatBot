function y = PredictRankSVM(args)
%PREDICTRANKSVM Predicts the rank of the card that should be played
%   Y = PREDICTRANKSVM(ARGS) is the prediction of the rank that should be
%   played. This function takes in a vector ARGS of features and outputs Y,
%   a single number that indicates which card should be played. x is a 1 x
%   42 array of features.
    
    load softmax_parameters.mat;
    load svm_parameters.mat;
    
    n_features = 42;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end
    
    % Softmax
    x(1,1) = 1;     
    p = exp(theta_rank'*(x'));
    p = p./sum(exp(theta_rank'*(x')));
    [~, y] = sort(p, 'descend');
    y4 = y(1);
    
    % SVM
    x = x(2:n_features);    	
    y1 = svmpredict(1, x, model_rank1, '-q');
    y2 = svmpredict(1, x, model_rank2, '-q');
    y3 = svmpredict(1, x, model_rank3, '-q');
    
    y = [y1 y2 y3 y4] - 1;
end
