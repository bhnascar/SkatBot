function [] = TestRankFile(filename)
% TESTRANKFILE Tests the rank file for consistency
%   USAGE: TestRankFile(filename). Filename has to be a CSV file that
%   contains the rank data as specified in the google docs. The labels must
%   come first in each row, from 0 to 10, and we must have 41 features.

    A = csvread(filename); % reads the matrix in the csv file
    [m, n] = size(A); % m is the number of training examples, n is the number of features
    y = A(:,1) + 1; % extracts the labels as a column vector (from 1 to 11)
    X = A(:,2:n); % sets X to be only features

    doIHaveThisCard = X(:, 9:19); % this matrix contains only the binary features that indicate whether I have card i 

    % Testing for illegal moves. An illegal move is defined when , for that
    % particular training example, the features indicate that I did not have
    % the card I chose to play.
    count_illegal = 0;
    bool_illegal = false(m,1);
    for i = 1:m
        if (doIHaveThisCard(i, y(i)) == 0)
            count_illegal = count_illegal+1;
            bool_illegal(i) = true;
        end
    end
    disp(['We found ' int2str(count_illegal) ' illegal moves in ' int2str(m) ' training examples']);
    illegal_labels = y(bool_illegal)

    % Testing for impossible moves. An impossible move is defined when, for
    % that particular training example, the features indicate that I had no
    % cards of that suit in my hand. Note that these could overlap with illegal
    % moves.
    totalCardsOfChosenSuit = sum(doIHaveThisCard,2);
    bool_impossible = (totalCardsOfChosenSuit == 0);
    disp(['We found ' int2str(sum(bool_impossible)) ' impossible moves in ' int2str(m) ' training examples']);
    impossible_labels = y(bool_impossible)

    % Testing for no choice. A no-choice move is defined when, for that
    % particular training example, I only had one card in my hand and I ended
    % up palying that card. Note that this does not overlap with impossible or
    % illegal moves
    bool_nochoice = ((totalCardsOfChosenSuit == 1) & (bool_illegal==0));
    disp(['We found ' int2str(sum(bool_nochoice)) ' no-choice moves in ' int2str(m) ' training examples']);
    nochoice_labels = y(bool_nochoice)
end


