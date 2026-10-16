void _DMA_StartTransfer(unsigned int dma)
{
	unsigned int *dmaregs = (void*)0x6410;
	unsigned int dmarec;

	dmarec = dma;

	if(dmaregs[dmarec+0x02]==0xD7B1 || dmaregs[dmarec+0x02]==0xD7B2) {
		unsigned char status;

		status = dmaregs[0x10];
		status &= ~0x10;
		if(dmaregs[dmarec+0x02]==0xD7B2) status |= 0x10;
		dmaregs[0x10] = status;

		dmaregs[dmarec+0x02] = 0xD7B0;
	}
}