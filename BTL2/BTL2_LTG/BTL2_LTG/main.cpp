#include <SDL.h>
#undef main
#include <SDL_ttf.h>
#include <iostream>
#include <string>

#define WIDTH 1600
#define HEIGHT 900
#define FONT_SIZE 32
#define SPEED 11
#define HIGH_SPEED 22
#define AUTO_PADDLE_SPEED 15 // Increased speed for auto-controlled paddle
#define SIZE 16
#define BALL_SPEED 22
#define HIGH_BALL_SPEED 44
#define PI 3.14159265358979323846

SDL_Renderer* renderer;
SDL_Window* window;
TTF_Font* font;
SDL_Color color;
bool running;
int frameCount, timerFPS, lastFrame, fps;
bool singlePlayer = true;

SDL_Rect l_paddle, r_paddle, ball, score_board;
float velX, velY;
std::string score;
int l_s, r_s;
bool turn;
bool l_hyperMode = false;
bool r_hyperMode = false;

void write(std::string text, int x, int y) {
    SDL_Surface* surface;
    SDL_Texture* texture;
    if (font == NULL) {
        fprintf(stderr, "error: font not found\n");
        exit(EXIT_FAILURE);
    }
    const char* t = text.c_str();
    surface = TTF_RenderText_Solid(font, t, color);
    texture = SDL_CreateTextureFromSurface(renderer, surface);
    score_board.w = surface->w;
    score_board.h = surface->h;
    score_board.x = x - score_board.w / 2;
    score_board.y = y - score_board.h / 2;
    SDL_FreeSurface(surface);
    SDL_RenderCopy(renderer, texture, NULL, &score_board);
    SDL_DestroyTexture(texture);
}

void showMenu();

void serve() {
    l_paddle.x = 32;
    l_paddle.y = (HEIGHT / 2) - (l_paddle.h / 2);
    r_paddle.y = l_paddle.y;
    r_paddle.x = WIDTH - r_paddle.w - 32;
    if (turn) {
        ball.x = l_paddle.x + (l_paddle.w * 4);
        velX = BALL_SPEED / 2;
    }
    else {
        ball.x = r_paddle.x - (r_paddle.w * 4);
        velX = -BALL_SPEED / 2;
    }
    ball.y = HEIGHT / 2;
    velY = 0;
    turn = !turn;

    // Wait for any key press to start the new round
    SDL_Event e;
    bool waiting = true;
    while (waiting) {
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_KEYDOWN) {
                waiting = false;
                break;
            }
        }
    }
}

void update() {
    int l_currentBallSpeed = l_hyperMode ? HIGH_BALL_SPEED : BALL_SPEED;
    int r_currentBallSpeed = r_hyperMode ? HIGH_BALL_SPEED : BALL_SPEED;

    if (SDL_HasIntersection(&ball, &l_paddle)) {
        double in = (l_paddle.y + (l_paddle.h / 2)) - (ball.y + (ball.h / 2));
        double nor = in / (l_paddle.h / 2);
        double b = nor * (5 * PI / 12);
        velX = l_currentBallSpeed * cos(b);
        velY = l_currentBallSpeed * -sin(b);
    }
    if (SDL_HasIntersection(&ball, &r_paddle)) {
        double in = (r_paddle.y + (r_paddle.h / 2)) - (ball.y + (ball.h / 2));
        double nor = in / (r_paddle.h / 2);
        double b = nor * (5 * PI / 12);
        velX = -r_currentBallSpeed * cos(b);
        velY = r_currentBallSpeed * -sin(b);
    }
    if (singlePlayer) {
        if (ball.y > (r_paddle.y + (r_paddle.h / 2))) r_paddle.y += AUTO_PADDLE_SPEED;
        if (ball.y < (r_paddle.y + (r_paddle.h / 2))) r_paddle.y -= AUTO_PADDLE_SPEED;
    }
    if (ball.x < 0) { r_s++; serve(); }
    if (ball.x + ball.w > WIDTH) { l_s++; serve(); }
    if (ball.y < 0 || ball.y + ball.h > HEIGHT) velY = -velY;
    ball.x += velX;
    ball.y += velY;
    score = std::to_string(l_s) + "   " + std::to_string(r_s);
    if (l_paddle.y < 0) l_paddle.y = 0;
    if (l_paddle.y + l_paddle.h > HEIGHT) l_paddle.y = HEIGHT - l_paddle.h;
    if (l_paddle.x < 0) l_paddle.x = 0; // Prevent paddle from moving out of bounds
    if (l_paddle.x + l_paddle.w > WIDTH) l_paddle.x = WIDTH - l_paddle.w; // Prevent paddle from moving out of bounds
    if (r_paddle.y < 0) r_paddle.y = 0;
    if (r_paddle.y + r_paddle.h > HEIGHT) r_paddle.y = HEIGHT - r_paddle.h;
    if (r_paddle.x < 0) r_paddle.x = 0; // Prevent right paddle from moving out of bounds
    if (r_paddle.x + r_paddle.w > WIDTH) r_paddle.x = WIDTH - r_paddle.w; // Prevent right paddle from moving out of bounds
}

void input() {
    SDL_Event e;
    const Uint8* keystates = SDL_GetKeyboardState(NULL);
    while (SDL_PollEvent(&e)) if (e.type == SDL_QUIT) running = false;
    if (keystates[SDL_SCANCODE_ESCAPE]) {
        running = false;
        showMenu();
    }

    int l_currentSpeed = l_hyperMode ? HIGH_SPEED : SPEED;
    int r_currentSpeed = r_hyperMode ? HIGH_SPEED : SPEED;

    if (singlePlayer) {
        if (keystates[SDL_SCANCODE_UP]) l_paddle.y -= l_currentSpeed;
        if (keystates[SDL_SCANCODE_DOWN]) l_paddle.y += l_currentSpeed;
        if (keystates[SDL_SCANCODE_LEFT]) l_paddle.x -= l_currentSpeed; // Move paddle left
        if (keystates[SDL_SCANCODE_RIGHT]) l_paddle.x += l_currentSpeed; // Move paddle right
    }
    else {
        if (keystates[SDL_SCANCODE_W]) l_paddle.y -= l_currentSpeed;
        if (keystates[SDL_SCANCODE_S]) l_paddle.y += l_currentSpeed;
        if (keystates[SDL_SCANCODE_A]) l_paddle.x -= l_currentSpeed; // Move paddle left
        if (keystates[SDL_SCANCODE_D]) l_paddle.x += l_currentSpeed; // Move paddle right

        if (keystates[SDL_SCANCODE_UP]) r_paddle.y -= r_currentSpeed;
        if (keystates[SDL_SCANCODE_DOWN]) r_paddle.y += r_currentSpeed;
        if (keystates[SDL_SCANCODE_LEFT]) r_paddle.x -= r_currentSpeed; // Move paddle left
        if (keystates[SDL_SCANCODE_RIGHT]) r_paddle.x += r_currentSpeed; // Move paddle right
    }

    if (keystates[SDL_SCANCODE_SPACE]) l_hyperMode = true; else l_hyperMode = false;
    if (keystates[SDL_SCANCODE_RETURN]) r_hyperMode = true; else r_hyperMode = false;
}

void render() {
    SDL_SetRenderDrawColor(renderer, 0x00, 0x00, 0x00, 255);
    SDL_RenderClear(renderer);

    frameCount++;
    int timerFPS = SDL_GetTicks() - lastFrame;
    if (timerFPS < (1000 / 60)) {
        SDL_Delay((1000 / 60) - timerFPS);
    }

    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, 255);
    SDL_RenderFillRect(renderer, &l_paddle);
    SDL_RenderFillRect(renderer, &r_paddle);
    SDL_RenderFillRect(renderer, &ball);
    write(score, WIDTH / 2 + FONT_SIZE, FONT_SIZE * 2);

    if (l_hyperMode) {
        write("Hyper Mode", l_paddle.x + l_paddle.w / 2, l_paddle.y - FONT_SIZE);
    }
    if (r_hyperMode) {
        write("Hyper Mode", r_paddle.x + r_paddle.w / 2, r_paddle.y - FONT_SIZE);
    }

    SDL_RenderPresent(renderer);
}

void showMenu() {
    bool menuRunning = true;
    SDL_Event e;

    while (menuRunning) {
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) {
                running = false;
                menuRunning = false;
            }
            if (e.type == SDL_KEYDOWN) {
                if (e.key.keysym.sym == SDLK_1) {
                    singlePlayer = true;
                    menuRunning = false;
                }
                if (e.key.keysym.sym == SDLK_2) {
                    singlePlayer = false;
                    menuRunning = false;
                }
                if (e.key.keysym.sym == SDLK_3) {
                    running = false;
                    menuRunning = false;
                }
            }
        }

        SDL_SetRenderDrawColor(renderer, 0x00, 0x00, 0x00, 255);
        SDL_RenderClear(renderer);

        write("Pong Game", WIDTH / 2, HEIGHT / 4);
        write("Press 1 for Single Player", WIDTH / 2, HEIGHT / 2);
        write("Press 2 for 1v1", WIDTH / 2, HEIGHT / 2 + FONT_SIZE * 2);
        write("Press 3 to Exit", WIDTH / 2, HEIGHT / 2 + FONT_SIZE * 4);

        SDL_RenderPresent(renderer);
    }
}

int main() {
    if (SDL_Init(SDL_INIT_EVERYTHING) < 0) std::cout << "Failed at SDL_Init()" << std::endl;
    if (SDL_CreateWindowAndRenderer(WIDTH, HEIGHT, SDL_WINDOW_FULLSCREEN, &window, &renderer) < 0) std::cout << "Failed at SDL_CreateWindowAndRenderer()" << std::endl;
    SDL_SetWindowTitle(window, "Pong");
    SDL_ShowCursor(0);

    TTF_Init();
    font = TTF_OpenFont("Peepo.ttf", FONT_SIZE);

    running = 1;
    l_s = r_s = 0;
    static int lastTime = 0;
    l_paddle.x = 32; l_paddle.h = HEIGHT / 4; l_paddle.y = (HEIGHT / 2) - (l_paddle.h / 2); l_paddle.w = 12;
    r_paddle = l_paddle; r_paddle.x = WIDTH - r_paddle.w - 32;
    color.r = 255;
    color.g = 255;
    color.b = 255;
    ball.w = ball.h = SIZE;

    showMenu();
    serve();

    while (running) {
        lastFrame = SDL_GetTicks();
        if (lastFrame >= (lastTime + 1000)) {
            lastTime = lastFrame;
            fps = frameCount;
            frameCount = 0;
        }

        update();
        input();
        render();
    }
    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}

