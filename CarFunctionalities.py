def draw(window, images, player_car):
    WINDOW.fill(white)
    for image, positon in images:
        window.blit(image,positon)
    
    player_car.drawCar(window)
    pygame.display.update()


def move_player(car):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT]:
        car.rotate(left=True, right=False)
    if keys[pygame.K_RIGHT]:
        car.rotate(right=True, left=False)
    if keys[pygame.K_UP]:
        moved = True
        car.move_forward()
    if keys[pygame.K_DOWN]:
        if not keys[pygame.K_UP]:
            moved = True
            car.move_backward()

    if not moved:
        car.slow_down()