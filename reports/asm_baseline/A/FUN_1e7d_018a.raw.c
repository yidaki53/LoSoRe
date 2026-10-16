static int
check_key(struct w6692_hw *card)
{
	unsigned char resp[10];

	resp[0] = 0xff;
	resp[1] = 0xff;
	resp[2] = 0xff;
	resp[3] = 0xff;
	resp[4] = 0xff;
	resp[5] = 0xff;
	resp[6] = 0xff;
	resp[7] = 0xff;
	resp[8] = 0xff;
	resp[9] = 0xff;

	W6692_fill_hdr(&card->MsgHdr, 0x182, 0x00);
	w6692_send_msg(card);

	W6692_fill_hdr(&card->MsgHdr, 0x182, 0x00);
	resp[0] = W6692_send_recv_msg(card, 0x41, 0x01, 0xff, resp);
	resp[1] = W6692_send_recv_msg(card, 0x49, 0x00, 0xff, resp);
	resp[2] = W6692_send_recv_msg(card, 0x44, 0x00, 0xff, resp);
	resp[3] = W6692_send_recv_msg(card, 0x48, 0x00, 0xff, resp);

	if (resp[0] == 0x00 || resp[1] == 0xff || resp[2] == 0xff ||
	    resp[3] == 0xff)
		return 0;

	return 1;
}