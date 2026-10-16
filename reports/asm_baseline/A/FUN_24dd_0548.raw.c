static void
draw_cursor(struct vt_window *vw, int col, int row)
{
	unsigned char *p;
	int x, y;

	p = vw->vw_buffer + (row * vw->vw_stride);
	p += col;

	if (*p == 0) {
		/* Clear the cursor area. */
		for (y = 0; y < 15; y++)
			for (x = 0; x < 14; x++)
				p[y * vw->vw_stride + x] = ' ';
	}
}