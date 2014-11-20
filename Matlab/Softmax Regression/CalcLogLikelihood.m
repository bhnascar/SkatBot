function ll = CalcLogLikelihood(X, Y, theta, C)
%CALCLOGLIKELIHOOD Calculates the log-likelihood of the data under a multinomial regression model
%  LL = CALCLOGLIKELIHOOD(X, Y, THETA, C) is the log likelihood of the
%  examples in X (m x n matrix) with the labels in y (m x 1 vector). THETA
%  is the parameter of the distribution and C is the constant used for
%  Bayesian statistics (C = 0 means no prior distribution)
    
    [m,~] = size(X); % m = number of training examples
    [~,k] = size(theta); % k = number of features
    
    ll = -C*sum(sum(theta.^2)); % Bayesian term
    Xt = X';
        
    for i = 1:m % loops through each training example
        x = Xt(:,i); % little x: the current training example
        ll = ll - log(sum(exp(theta'*x)));
        bool = (Y(i) == 1:k);
        ll = ll + bool*(theta'*x);
    end
end

