function [accuracy, illegal] = EvaluateSVMModel(X, Y, model, s)
%EVALUATESVMMODEL Tests the trained SVM model on a dataset
%   [ACC, ILLEGAL] = EVALUATEHYPOTHESIS(X, Y, THETA, THRESHOLD, S)
%   evaluates the current SVM model (represented by the struct MODEL)
%   on the dataset given by matrix X (m x n) and labels Y (m x 1). S 
%   is a character: use 's' for suit and 'r' for rank.

    [num_validate, ~] = size(X);    
    
    % Runs the SVM prediction model
    y_predicted = svmpredict(Y, X, model, '-q');
    
    accuracy = mean(y_predicted == Y);
    
    illegal = 0; 
    % This calculates the offset that determines how many cards of that label I have
    if (s == 's') 
        offset = 1;
    else
        offset = 9;
    end
    for i = 1:num_validate
        if (X(i, y_predicted(i)+offset) == 0)
            illegal = illegal + 1;
        end
    end    
    illegal = illegal/num_validate;
end

