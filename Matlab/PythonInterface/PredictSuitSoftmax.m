function y = PredictSuitSoftmax(args)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSOFTMAX(ARGS) is the prediction of the suit that should be
%   played. This function takes in a vector x of features and outputs y,
%   an array of 4 numbers between 0 and 3. The first number is the
%   algorithm's best guess, the second one is its second choice, etc. ARGS is
%   a 1x30 array.

    load parameters.mat;
    
    n_features = 30;
    x = zeros(1, n_features);
    
    fields = fieldnames(args);
    for i = 1:numel(fields)
        x(i) = args.(['arg', int2str(i)]);
    end            
    x(1,1) = 1;
     
    p = exp(theta_suit'*(x'));
    p = p./sum(exp(theta_suit'*(x')));
    [~, y] = sort(p, 'descend');
    y = y-1; 
end

