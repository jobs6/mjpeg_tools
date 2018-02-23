import os, pygame, io

screen = pygame.display.set_mode((444,250+100)) 
clock = pygame.time.Clock()

stream=open('out.mp4','rb')
bytes=''
frame = 1
frame_size = [0 for i in range(444)]
pause = 0
fps = 25
save = 0
play_once = 0

while 1:

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
            exit()
       if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_SPACE:
                pause = pause^1
            if event.key == pygame.K_UP:
                fps = min(fps+5,120)
                print(fps)
            if event.key == pygame.K_DOWN:
                fps = max(fps-5,5)
                print(fps)
            if event.key == pygame.K_RIGHT:
                play_once = 1
                pause = 0
            if event.key == pygame.K_LEFT:
                print()
            if event.key == pygame.K_RETURN and pause:
                save = 1

   if not pause:
        screen.fill((0,0,0))
        count = stream.read(1024)

        if len(count) == 0:
            exit()

        bytes += count
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a!=-1 and b!=-1:
            jpeg = bytes[a:b+2]
            bytes= bytes[b+2:]

            frame_size = frame_size[1:] + [len(jpeg)]
            print(350-(frame_size[-1]>>8))
            #print(str(len(jpeg))+' '+str(frame))
            
            for x in range(444):
                pygame.draw.line(screen,(0,200,0),(x,350),(x,350-(frame_size[x]>>8)) )

            pic = io.BytesIO(jpeg)
            img = pygame.image.load(pic) 
            screen.blit(img,(0,0))
            pygame.display.flip()

            if play_once:
                pause = 1
                play_once = 0

            frame += 1
            clock.tick(fps)
   else:
       if save:
            f = open(str(frame)+'.jpeg','wb')
            f.write(jpeg)
            f.close()
            save = 0

       clock.tick(10)
