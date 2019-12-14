// This C module provides utility functions to create a UDP socket.

#ifndef SOCKET_H
#define SOCKET_H

#include <sys/socket.h>

void initializeUdpServer(unsigned int port);

// Returns the destination socket address to respond to.
struct sockaddr_in receiveThroughUdpServer(char *buffer, unsigned int maxLen);

// Requires the destination socket address from the received message.
void sendThroughUdpServer(struct sockaddr_in sktDestination, char *message);

void closeUdpServer();

#endif