// This C source file provides utility functions to create a UDP socket.

#include <fcntl.h> // For open()
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>  // For close()

#include "../include/socket.h"

static bool initialized = false;
static int socketDescriptor = 0;

void initializeUdpServer(unsigned int port) {
  struct sockaddr_in skt;
  memset(&skt, 0, sizeof(skt));

  // Set properites
  skt.sin_family = AF_INET;  // Allow connection from network
  skt.sin_addr.s_addr = htonl(INADDR_ANY);
  skt.sin_port = htons(port);

  // Create socket
  socketDescriptor = socket(PF_INET, SOCK_DGRAM, 0);
  bind(socketDescriptor, (struct sockaddr*) &skt, sizeof(skt));

  initialized = true;
}

struct sockaddr_in receiveThroughUdpServer(char *buffer, unsigned int maxLen) {
  if (!initialized) {
    perror("Socket: Cannot receive data before the UDP server is initialized.");
    exit(1);
  }
  else if (buffer == NULL) {
    perror("Socket: The given buffer to receive a message cannot be NULL.");
    exit(1);
  }

  // Receive data
  struct sockaddr_in sktSender;
  unsigned int sktLen = sizeof(sktSender);

  unsigned int bytes = recvfrom(
    socketDescriptor,
    buffer, maxLen,
    0, (struct sockaddr *) &sktSender, &sktLen
  );

  // Complete the input string
  int stringTermination = (bytes < maxLen) ? bytes : maxLen-1;
  buffer[stringTermination] = 0;

  return sktSender;
}

void sendThroughUdpServer(struct sockaddr_in sktDestination, char *message) {
  if (!initialized) {
    perror("Socket: Cannot send data before the UDP server is initialized.");
    return;
  }
  else if (message == NULL) {
    perror("Socket: The given message was NULL.");
    exit(1);
  }

  int sktLen = sizeof(sktDestination);
  sendto(
    socketDescriptor,
    message, strlen(message),
    0,
    (struct sockaddr *) &sktDestination, sktLen
  );
}

void closeUdpServer() {
  if (!initialized) {
    perror("Socket: No descriptor to send.");
    return;
  }

  close(socketDescriptor);
  socketDescriptor = 0;
  initialized = false;
}