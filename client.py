
def main():
    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_p())
    print('You are player ', player)
    while run:
        clock.tick(60)
        try:
            game = network.send('get')
        except:
            run = False
            print('Could not get a game\n')
            break

        if game.did_both_go():
            redraw_window(win, game, player)
            pygame.time.delay(1000)
            try:
                game = network.send('reset')
            except:
                run = False
                print('Could not get a game\n')
                break

            font = pygame.font.SysFont('Roboto', 90)
            if (game.determine_winner() == 1 and player == 1) or (game.determine_winner() == 0 and player == 0):
                text = font.render('YOU WON!!', 1, (255, 255, 0))
            elif game.determine_winner() == -1:
                text = font.render('IT\'S A TIE!', 1, (255, 0, 255))
            else:
                text = font.render('YOU LOST!!', 1, (255, 0, 0))

            win.blit(text, ((width / 2 - text.get_width() / 2), (height - text.get_height() / 2)))

            pygame.display.update()
            pygame.time.delay(5000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.are_players_connected():
                        if player == 0:
                            if not game.player1_went:
                                network.send(button.text)
                        else:
                            if not game.player2_went:
                                network.send(button.text)

        redraw_window(win, game, player)

