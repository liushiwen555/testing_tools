/*
 * @Author: zzsuki
 * @Date:   2020-03-30 17:19:55
 * @Last Modified by:   zzsuki
 * @Last Modified time: 2020-04-01 16:56:02
 */
/*usage: cc mem.c -o ***.out 后 使用./***.out 100 & 消耗对应数字MB单位的内存，释放时杀掉对应进程即可*/
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <windows.h>

#define B_SIZE (1024*1024)
#define TRUE 1
#define FALSE 0

char* simulate_memeory(float persent);

int main(int argc, char *argv[])
{
        unsigned int lock_number;
        char release_flag;
        int i;

        printf("How many MB Size you asking for? (Decimal is good to use)");
        scanf("%d", &lock_number);
        // 如果输入0
        if (lock_number == 0) {
                printf("\nZero is not a good number!!\n");
                return 1;
        }
        printf("\nFinal lock_number is %d", lock_number);
        char *buff[lock_number];
        for (i = 0; i < lock_number; i++){
            // malloc申请内存，1次申请1MB
            buff[i] = (char *)malloc(B_SIZE);
            if ((i + 1) % 500 == 0){
                printf("\nCurrent Memory Applied: %d MB..", i + 1);
            }
            // 使用内存
            for(int j = 1; j < B_SIZE; j++){
                if(j % 1024 == 0){
                    // buff[i][j] = buff[i][j-1]/8;
                    buff[i][j] = 'a';
                } else {
                    buff[i][j] = 'b';
                }
            }
        }
        // 释放内存
        wait_flag : printf("\nCan I release these memory now? Y/N ");
        scanf("%s", &release_flag);
        if (release_flag == 'Y'){
            printf("These Memory will be freed..\n");
            // 释放内存
            for(i = 0; i < lock_number; i++){
                free(buff[i]);
            }
            printf("Memory has been freed..\n");
            return 1;
        }else{
            goto wait_flag;
        }
        
        Sleep(100000);

}
