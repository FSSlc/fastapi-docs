https://leetcode.cn/problems/maximum-length-of-repeated-subarray/solution/wu-li-jie-fa-by-stg-2/
https://www.geeksforgeeks.org/check-whether-an-array-is-subarray-of-another-array/
https://leetcode.cn/problems/maximum-length-of-repeated-subarray/solution/hua-dong-chuang-kou-python-by-downupzi-ihfv/

```python
# Python3 program to check if an array is
# subarray of another array

# Function to check if an array is
# subarray of another array
def isSubArray(A, B, n, m):
	
	# Two pointers to traverse the arrays
	i = 0; j = 0;

	# Traverse both arrays simultaneously
	while (i < n and j < m):

		# If element matches
		# increment both pointers
		if (A[i] == B[j]):

			i += 1;
			j += 1;

			# If array B is completely
			# traversed
			if (j == m):
				return True;
		
		# If not,
		# increment i and reset j
		else:
			i = i - j + 1;
			j = 0;
		
	return False;

# Driver Code
if __name__ == '__main__':
	A = [ 2, 3, 0, 5, 1, 1, 2 ];
	n = len(A);
	B = [ 3, 0, 5, 1 ];
	m = len(B);

	if (isSubArray(A, B, n, m)):
		print("YES");
	else:
		print("NO");

# This code is contributed by Rajput-Ji
```

```python
def findLength(nums1, nums2) -> int:
    res = 0
    n1, n2 = len(nums1), len(nums2)

    def getLength(i, j): # 找对齐部分最长
        nonlocal res
        cur = 0
        while i < n1 and j < n2:
            if nums1[i] == nums2[j]:
                cur += 1
                res = max(res, cur)
            else:
                cur = 0
            i, j = i + 1, j + 1

    # 两个数组分别以自己的头怼另外一个数组一遍
    for j in range(n2): 
        getLength(0, j)
    for i in range(n1): 
        getLength(i, 0)
    return res
```
