function theta = TrainSoftmaxAscent(X, Y, k, C, learn_rate, N_max)
%TRAINSOFTMAX Trains the regression algorithm on data set 
%   THETA = TRAINSOFTMAX(X, Y, K, C, LEARN_RATE, N_max) will train the softmax
%   regression algorithm on dataset given by X (feature matrix) and Y
%   (labels, starting at 1). The algorithm assumes K different classes (K=2
%   for logistic regression) and a constant C controlling the Bayesian prior
%   (C=0 means no prior). Batch gradient ascent is used, with learning 
%   rate LEARN_RATE and N_MAX as the maximum number of steps. We stop
%   iterating if, after N iterations, the log likelihood changes by less
%   than tol (default: 100, 0.001)

    % Error Checking
    [m,n] = size(X);

    if (m ~= size(Y))
        error('Size of X and Y do not match');
    end
    if (learn_rate <= 0 || N_max < 1)
        error('Learning rate must be positive and N_max must be at least 1');
    end
    if (C < 0)
        error('C must not be negative');
    end
    if (min(Y) <= 0)
        error('The labels in Y must start from 1 (no 0 or negative numbers)');
    end
    if (k <= 1)
        error('We must have at least two classes (k >= 2)');
    end
    if (max(Y) > k)
        error('Some labels in Y exceed the number of classes k');
    end
    

    % Initialize theta    
    theta = zeros(n,k);
    Xt = X'; % the transpose of matrix X
    N = 100;
    tol = 0.001;
    oldL = CalcLogLikelihood(X, Y, theta, C);
    
    % Run Gradient Ascent
    for times = 1:N_max
        %times
        for p = 1:k-1
            bool = (Y == p);
            thetaX = (theta'*Xt)';
            termA = (exp(thetaX(:,p))./sum(exp(thetaX), 2)); % see notes
            % Grad is the (nx1) vector representing the gradient
            Grad = sum(Xt(:,bool), 2) - Xt*termA - 2*C*theta(:,p);
            
            theta(:,p) = theta(:,p) + learn_rate*Grad;
        end
        %CalcLogLikelihood(X, Y, theta, C)
        if (mod(times, N) == 0)
            newL = CalcLogLikelihood(X, Y, theta, C);
            if (abs((newL-oldL)/oldL) < tol) % if likelihood changes by less than 0.1% after N iterations
                break;
            end
            oldL = newL;
        end
    end    
end

