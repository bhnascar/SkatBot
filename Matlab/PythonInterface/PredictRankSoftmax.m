function y = PredictRankSoftmax(args)
%PREDICTRANKSOFTMAX Predicts the rank of the card that should be played
%   Y = PREDICTRANKSOFTMAX(ARGS) is the prediction of the rank that should be
%   played. This function takes in a vector ARGS of features and outputs Y,
%   an array of 11 numbers between 0 and 10. The first number is the
%   algorithm's best guess, the second one is its second choice, etc. ARGS is
%   a 1x42 feature vector

    load softmax_parameters.mat;
    
    n_features = 42;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    x(1,1) = 1;

    p = exp(theta_rank'*(x'));
    p = p./sum(exp(theta_rank'*(x')));
    [~, y] = sort(p, 'descend');
    y = y-1;
end

