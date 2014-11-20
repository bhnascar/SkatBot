function theta = TrainSoftmaxNewton(X, Y, k, C, ~, N_steps)
%TRAINSOFTMAX Trains the regression algorithm on data set 
%   THETA = TRAINSOFTMAX(X, Y, K, C, N_STEPS) will train the softmax
%   regression algorithm on dataset given by X (feature matrix) and Y
%   (labels, starting at 1). The algorithm assumes K different classes (K=2
%   for logistic regression) and a constant C controlling the Bayesian prior
%   (C=0 means no prior). Newton's method is used with N_steps (10-15 is 
%   is usually enough for convergence). Note that warning for nearly
%   singular matrix is turned off.

    % Error Checking
    [m,n] = size(X);

    if (m ~= size(Y))
        error('Size of X and Y do not match');
    end
    if (N_steps < 1)
        error('N_steps must be at least 1');
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
    warning('off', 'MATLAB:nearlySingularMatrix'); % turns annoying warning off
   
    % Run Newton's method
    for times = 1:N_steps
        for p = 1:k-1 % for each of the parameters theta
            thetaX = (theta'*Xt)';
            termA = (exp(thetaX(:,p))./sum(exp(thetaX), 2)); % see notes
            termB = termA.*(termA-1); % see notes
            bool = (Y == p);
            
            % Grad is the (nx1) vector representing the gradient
            Grad = sum(Xt(:,bool), 2) - Xt*termA - 2*C*theta(:,p); 
            
            % The nxn matrix containing the Hessian
            Hessian = Xt*SingletonMultiply(termB, X) - 2*C*eye(n);
            
            % Updates according to Newton's method
            theta(:,p) = theta(:,p) - Hessian\Grad; 
        end        
        %CalcLogLikelihood(X, Y, theta, C)
    end
    
    % This function takes in a (m x 1) array v and dot-multiplies it by each
    % column of matrix A (m x n), producing matrix B (m x n)
    function B = SingletonMultiply(v, A)
        for j = n:-1:1
            B(:,j) = v.*A(:,j);
        end
end
        
end





