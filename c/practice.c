#include <stdio.h>  // 표준 입출력 라이브러리

#define MAX_SIZE 100  // 입력 가능한 최대 데이터 수 (2바이트 단위)

// 체크섬 계산 함수 (1의 보수 덧셈 방식)
unsigned short calculate_checksum(unsigned short data[], int size) {
    unsigned int sum = 0;  // 합계를 저장할 변수 (carry 처리를 위해 32비트)

    // 모든 2바이트 데이터에 대해 반복하면서 합산
    for (int i = 0; i < size; i++) {
        sum += data[i];

        // 만약 합이 16비트를 초과하면 (carry 발생 시)
        // 상위 비트를 하위에 다시 더해주는 방식으로 처리 (1의 보수 덧셈 규칙)
        if (sum > 0xFFFF) {
            sum = (sum & 0xFFFF) + 1;
        }
    }

    // 최종 합에 대해 1의 보수를 취해 체크섬 반환
    // (~sum)은 비트를 반전시키고, 0xFFFF와 AND 연산하여 16비트로 자름
    return ~sum & 0xFFFF;
}

int main() {
    int size;  // 사용자로부터 입력받을 데이터 개수
    unsigned short data[MAX_SIZE];  // 2바이트 정수 데이터를 저장할 배열

    // 사용자에게 데이터 개수 입력 받기
    printf("2바이트 정수 데이터 크기 입력: ");
    scanf("%d", &size);

    // 입력 크기가 배열 최대값을 넘으면 종료
    if (size > MAX_SIZE) {
        printf("데이터 크기가 너무 큽니다 (최대 %d)\n", MAX_SIZE);
        return 1;
    }

    // 사용자가 입력한 개수만큼 16진수 형태로 데이터 입력 받기
    printf("앞에 입력한 크기 만큼 2바이트 정수를 16진수 값으로 입력:\n");
    for (int i = 0; i < size; i++) {
        printf("0x");  // 입력을 보기 좋게 하기 위해 출력
        scanf("%hx", &data[i]);  // "%hx"는 16진수로 unsigned short 입력 받기
    }

    // 체크섬 계산 함수 호출
    unsigned short checksum = calculate_checksum(data, size);

    // 결과 출력 (대문자 16진수 형식으로 출력)
    printf("\n체크섬 결과: %04X\n", checksum);

    return 0;
}
