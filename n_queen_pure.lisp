(defun safe-p (board row col)
  (labels ((safe-p-helper (board row col i)
             (if (eq i row)
                 t
                 (let ((j (car (nth i board))))
                   (if (or (eq j col) (eq (abs (- j col)) (- row i)))
                       nil
                       (safe-p-helper board row col (1+ i)))))))
    (safe-p-helper board row col 0)))

(defun solve-n-queens (n)
  (labels ((place-queen (board row)
             (if (eq row n)
                 (cons (reverse board) solutions)
                 (place-queen-helper board row 0)))
           (place-queen-helper (board row col)
             (if (eq col n)
                 solutions
                 (if (safe-p board row col)
                     (place-queen (cons (cons row col) board) (1+ row))
                     (place-queen-helper board row (1+ col))))))
    (place-queen nil 0)))

(defun print-board (solution)
  (labels ((print-row (row n)
             (if (eq n 0)
                 (terpri)
                 (progn
                   (if (eq (car row) (1- n))
                       (format t "Q ")
                       (format t ". "))
                   (print-row row (1- n))))))
    (dolist (row solution)
      (print-row row (length solution)))))

(defun print-solutions (solutions)
  (format t "Found ~D solutions:~%" (length solutions))
  (dolist (solution solutions)
    (print-board solution)
    (terpri)))

(let ((solutions (solve-n-queens 8)))
  (print-solutions solutions))