# assignment operators
# binary operators
# transposition

C = -A;     # assignemnt with unary expression
C = B' ;    # assignemnt with matrix transpose
C = A+B ;   # assignemnt with binary addition
C = A-B ;   # assignemnt with binary substraction
C = A*B ;   # assignemnt with binary multiplication
C = A/B ;   # assignemnt with binary division
C = A.+B ;  # add element-wise A to B
C = A.-B ;  # substract B from A 
C = A.*B ;  # multiply element-wise A with B
C = A./B ;  # divide element-wise A by B

C += B ;  # add B to C 
C -= B ;  # substract B from C 
C *= A ;  # multiply A with C
C /= A ;  # divide A by C





# special functions, initializations

A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

# initialize 3x3 matrix with specific values
E1 = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;

A[1,3] = 0 ;




x=0;

for a=1:10 {
x=0;
continue;
}

x = ones(1);

break;

E1 = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;
E2 = [1,2,3,4;
     1,2,3,4;
     1,2,3,4 ];

E3 = E1 .+ E2;

A[1] = 0 ;

z = 1 + 1;

print x;