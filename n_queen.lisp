(defun safe-p (board row col)
  (loop for i from 0 below row
        for j = (aref board i)
        always (and (/= j col) (/= (abs (- j col)) (- row i)))))

(defun solve-n-queens (n)
  (let ((solutions '()))
    (labels ((place-queen (board row)
               (if (= row n)
                   (push (reverse (coerce board 'list)) solutions)
                   (loop for col from 0 below n
                         when (safe-p board row col)
                         do (setf (aref board row) col)
                            (place-queen board (1+ row))))))
      (place-queen (make-array n :initial-element -1) 0))
    solutions))

(defun print-board (solution)
  (dolist (row solution)
    (dotimes (i (length solution))
      (format t (if (= i row) "Q " ". ")))
    (terpri)))

(defun print-solutions (solutions)
  (format t "Found ~D solutions:~%" (length solutions))
  (dolist (solution solutions)
    (print-board solution)
    (terpri)))

(let ((solutions (solve-n-queens 8)))
  (print-solutions solutions))
