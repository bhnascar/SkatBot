function [y] = PredictSuitSoftmax(args)
%PREDICTSUITSOFTMAX Predicts the suit of the card that should be played
%   Y = PREDICTSUITSOFTMAX(X) is the prediction of the suit that should be
%   played. This function takes in a vector x of features and outputs y,
%   an array of 4 numbers between 1 and 4. The first number is the
%   algorithm's best guess, the second one is its second choice, etc. x is
%   a 1x30 array.

    Initialize();
    fields = fieldnames(args);
    x = zeros(1, 30);
    for i = 1:numel(fields)
        x(i) = args.(fields{i});
    end            
    x(1,1) = 1;

    p = exp(theta_suit'*(x')); % this contains the probability of each of k classes being picked
    p = p./sum(exp(theta'*xi));
    [~, y] = sort(p, 'descend');
end

