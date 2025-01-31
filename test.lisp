(defun safe-p (board row col)
  (loop for i from 0 below row
        for j = (aref board i)
        always (and (/= j col) (/= (abs (- j col)) (- row i)))))