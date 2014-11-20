function [acc, high_conf, bad_mist, illegal] = EvaluateHypothesis(X, Y, theta, threshold, s)
%EVALUATEHYPOTHESIS Tests the trained parameter on a dataset
%   [ACC, HIGH_CONF, BAD_MIST] = EVALUATEHYPOTHESIS(X, Y, THETA, THRESHOLD, S)
%   evaluates the current multinomial hypothesis (represented by the 
%   parameter vector THETA) on the dataset given by matrix X (m x n) and
%   labels Y (m x 1). Note that THETA is a matrix (n x k), where k is the
%   number of buckets our multinomial hypothesis accepts. THRESHOLD should
%   be a high probability used to decide whether a prediction is made with
%   high confidence and whether the algorithm commited a bad mistake. S is
%   a character: use 's' for suit and 'r' for rank

    [num_validate, ~] = size(X);
    acc = 0;
    high_conf = 0;
    bad_mist = 0;
    illegal = 0;
    if (s == 's') % suit
        offset = 1;
    else % rank
        offset = 9;
    end
    
    for i = 1:num_validate
        xi = X(i,:)';
        p = exp(theta'*xi); % this contains the probability of each of k classes being picked
        p = p./sum(exp(theta'*xi));
        [prob, index] = max(p);
        if (index == Y(i))
            acc = acc+1;
        end
        if (prob > threshold)
            high_conf = high_conf + 1;
            if (index ~= Y(i))
                bad_mist = bad_mist + 1;
            end            
        end
      
        if (xi(index+offset) == 0)
            illegal = illegal + 1;
        end            
    end
    
    acc = acc/num_validate;
    high_conf = high_conf/num_validate;
    bad_mist = bad_mist/num_validate;
    illegal = illegal/num_validate;
end

