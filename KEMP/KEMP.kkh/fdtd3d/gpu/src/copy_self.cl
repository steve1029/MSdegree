PRAGMA_fp64

__kernel void copy_self(int nx, int ny, int nz, __global DTYPE *f) {
	int gid = get_global_id(0);
    int idx0, idx1;

	if( gid < NMAX ) {
        idx0 = IDX0;
        idx1 = IDX1;

	   	f[idx1] = f[idx0];
	}
} 
