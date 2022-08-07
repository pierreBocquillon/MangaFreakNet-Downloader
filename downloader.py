import os
import zipfile
from cmath import inf
import requests
from bs4 import BeautifulSoup
from PIL import Image
import shutil
import cv2

baseUrl = "https://w13.mangafreak.net/Manga/"
maxDownloadStep = 10
reversed = False
split = True
downloadLocation = "./downloads/"
zipSuffix =  "/zip/"
extractSuffix =  "/images/"
pagesSuffix =  "/pages/"

options = ["menu", "change", "download", "extract", "build", "clean", "quit"]
currrentOptionIndex = 1

mangaName = ""

def clearConsole():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
    return

while options[currrentOptionIndex] != "quit":
    
    clearConsole()

    if options[currrentOptionIndex] == "menu":
        optionTexts = dict()
        optionTexts["change"] = "Change current manga ( current: " + mangaName + " )"
        optionTexts["download"] = "Download new chapters for " + mangaName
        optionTexts["extract"] = "Extract pages from downloaded zip for " + mangaName
        optionTexts["build"] = "Build pdf from extracted pages for " + mangaName
        optionTexts["clean"] = "Clean all downloaded files (it will keep only zip and pdf files)"
        optionTexts["quit"] = "Quit application"
        print("Options:")
        for i in range(len(options)):
            if i != currrentOptionIndex:
                print(str(i) + " : " + optionTexts[options[i]])
        currrentOptionIndex = int(input("What do you want to do ? "))
    
    elif options[currrentOptionIndex] == "change":
        loadAnswer = input("Add new manga ? (y/n) ")
        if loadAnswer.lower() == "y" or loadAnswer.lower() == "yes" :
            mangaName = input("URL : " + baseUrl)
        else :
            clearConsole()
            print("Existing manga :")
            for i in range(len(os.listdir(downloadLocation))):
                print(str(i) + " : " + os.listdir(downloadLocation)[i])
            print("")
            mangaIndex = input("Selects the corresponding number ? ")
            mangaName = os.listdir(downloadLocation)[int(mangaIndex)]

        url = baseUrl + mangaName
        location = downloadLocation + url.split("/")[-1] + "/zip/"
        extractLocation = downloadLocation + url.split("/")[-1] + "/images/"
        pagesLocation = downloadLocation + url.split("/")[-1] + "/pages/"
        pdfLocation = downloadLocation + url.split("/")[-1] + "/" + url.split("/")[-1] + ".pdf"
        
        currrentOptionIndex = 0

    elif options[currrentOptionIndex] == "download":
        firstChapter = int(input("First chapter: "))
        clearConsole()
        lastChapter = int(input("Last chapter: "))

        pagrRawHtml = requests.get(url).text

        html = BeautifulSoup(pagrRawHtml, "html.parser")
        manga_series_list = html.find("div", class_="manga_series_list")
        download_links = manga_series_list.select("a[download]")

        links = []

        for link in download_links:
            links.append(link["href"])

        selected_links = links[firstChapter-1:lastChapter]

        if not os.path.exists(location):
            os.makedirs(location)
        
        stepCount = len(selected_links)
        step = 0

        for link in selected_links:
            step += 1
            contentArray = []

            for i in range(maxDownloadStep):
                res = requests.get(link)
                if res.status_code == 200:
                    contentArray.append(res.content)
            
            if len(contentArray) == 0:
                print("Error: " + link)
                continue
            else :
                minSize = float('inf')
                content = ""
                
                for content in contentArray:
                    if len(content) < minSize:
                        minSize = len(content)
                        content = content
                chapterNumber = link.split("/")[-1].split("_")[-1]
                fullChapterName = chapterNumber
                numeric_filter = filter(str.isdigit, chapterNumber)
                numeric_string = "".join(numeric_filter)
                chapterNumber = numeric_string
                chapterSuffix = fullChapterName.replace(chapterNumber, "")

                if len(chapterNumber) == 1:
                    chapterNumber = "00" + chapterNumber
                elif len(chapterNumber) == 2:
                    chapterNumber = "0" + chapterNumber

                filePath = location + "Chapter_" + chapterNumber + chapterSuffix + ".zip"
                open(filePath, "wb").write(res.content)
            
            clearConsole()
            currentNormalizedStep = int((step / stepCount) * 30)
            remaingNormalizedStep = 30 - currentNormalizedStep

            downloadBar = "["
            for i in range(currentNormalizedStep):
                downloadBar += "#"
            for i in range(remaingNormalizedStep):
                downloadBar += "-"
            downloadBar += "] "

            print("Downloading " + downloadBar + " (" + str(step) + "/" + str(stepCount) + ")")

        currrentOptionIndex = 0

    elif options[currrentOptionIndex] == "extract":
        
        splitAnswer = input("Do you need to split the pages ? (y/n) ")
        if splitAnswer.lower() == "y" or splitAnswer.lower() == "yes" :
            split = True
        else :
            split = False

        if not os.path.exists(location):
            os.makedirs(location)
        
        if not os.path.exists(extractLocation):
            os.makedirs(extractLocation)
        
        if not os.path.exists(pagesLocation):
            os.makedirs(pagesLocation)
        
        for file in os.listdir(extractLocation):
            shutil.rmtree(extractLocation + file)

        zipStepCount = len(os.listdir(location))
        zipStep = 0

        currentZipNormalizedStep = int((zipStep / zipStepCount) * 30)
        remaingZipNormalizedStep = 30 - currentZipNormalizedStep

        extractBar = "["
        for i in range(currentZipNormalizedStep):
            extractBar += "#"
        for i in range(remaingZipNormalizedStep):
            extractBar += "-"
        extractBar += "] "

        for chapter in os.listdir(location):
            zipStep += 1

            with zipfile.ZipFile(location + chapter, 'r') as zip_ref:
                zip_ref.extractall(extractLocation + chapter.replace(".zip", "") + "/")

            clearConsole()
            currentZipNormalizedStep = int((zipStep / zipStepCount) * 30)
            remaingZipNormalizedStep = 30 - currentZipNormalizedStep

            extractBar = "["
            for i in range(currentZipNormalizedStep):
                extractBar += "#"
            for i in range(remaingZipNormalizedStep):
                extractBar += "-"
            extractBar += "] "

            print("Extracting " + extractBar + " (" + str(zipStep) + "/" + str(zipStepCount) + ")")
        
        pageStepCount = 0
        for chapter in os.listdir(extractLocation):
            pageStepCount += len(os.listdir(extractLocation + chapter))
        pageStep = 0
        
        currentPageNormalizedStep = int((pageStep / pageStepCount) * 30)
        remaingPageNormalizedStep = 30 - currentPageNormalizedStep

        pageBar = "["
        for i in range(currentPageNormalizedStep):
            pageBar += "#"
        for i in range(remaingPageNormalizedStep):
            pageBar += "-"
        pageBar += "] "

        for chapter in os.listdir(extractLocation):
            for page in os.listdir(extractLocation + chapter):
                pageStep += 1
                if not os.path.exists(pagesLocation + chapter + "/"):
                    os.makedirs(pagesLocation + chapter + "/")
                
                img = cv2.imread(extractLocation + chapter + "/" + page)
                
                if img is None:
                    continue

                if split :
                    width = img.shape[1]
                    cutPosition = int(width / 2)
                    leftPage = img[:, :cutPosition]
                    rightPage = img[:, cutPosition:]

                    pageName = page.split("_")[-1]
                    pageExtension = pageName.split(".")[1]
                    pageNumber = pageName.split(".")[0]

                    if len(pageNumber) == 1:
                        pageNumber = "00" + pageNumber
                    elif len(pageNumber) == 2:
                        pageNumber = "0" + pageNumber
                    
                    currentPageLocation = pagesLocation + chapter + "/" + pageNumber + "." + pageExtension

                    if reversed :
                        cv2.imwrite(currentPageLocation.replace("." + pageExtension, "_1." + pageExtension), leftPage)
                        cv2.imwrite(currentPageLocation.replace("." + pageExtension, "_2." + pageExtension), rightPage)
                    else :
                        cv2.imwrite(currentPageLocation.replace("." + pageExtension, "_2." + pageExtension), leftPage)
                        cv2.imwrite(currentPageLocation.replace("." + pageExtension, "_1." + pageExtension), rightPage)
                else :
                    pageName = page.split("_")[-1]
                    pageExtension = pageName.split(".")[1]
                    pageNumber = pageName.split(".")[0]

                    if len(pageNumber) == 1:
                        pageNumber = "00" + pageNumber
                    elif len(pageNumber) == 2:
                        pageNumber = "0" + pageNumber

                    currentPageLocation = pagesLocation + chapter + "/" + pageNumber + "." + pageExtension
                    cv2.imwrite(currentPageLocation, img)
                
            clearConsole()
            currentPageNormalizedStep = int((pageStep / pageStepCount) * 30)
            remaingPageNormalizedStep = 30 - currentPageNormalizedStep

            pageBar = "["
            for i in range(currentPageNormalizedStep):
                pageBar += "#"
            for i in range(remaingPageNormalizedStep):
                pageBar += "-"
            pageBar += "] "

            print("Page generation " + pageBar + " (" + str(pageStep*2) + "/" + str(pageStepCount*2) + ")")
        currrentOptionIndex = 0

    elif options[currrentOptionIndex] == "build":
        imageList = []

        buildStepCount = 0
        for chapter in os.listdir(pagesLocation):
            buildStepCount += len(os.listdir(pagesLocation + chapter))
        buildStep = 0

        currentBuildNormalizedStep = int((buildStep / buildStepCount) * 30)
        remaingBuildNormalizedStep = 30 - currentBuildNormalizedStep

        buildBar = "["
        for i in range(currentBuildNormalizedStep):
            buildBar += "#"
        for i in range(remaingBuildNormalizedStep):
            buildBar += "-"
        buildBar += "] "

        for chapter in os.listdir(pagesLocation):
            for page in os.listdir(pagesLocation + chapter):
                buildStep += 1
                image = Image.open(pagesLocation + chapter + "/" + page)
                image = image.convert("RGB")
                imageList.append(image)
            
            clearConsole()
            currentBuildNormalizedStep = int((buildStep / buildStepCount) * 30)
            remaingBuildNormalizedStep = 30 - currentBuildNormalizedStep

            buildBar = "["
            for i in range(currentBuildNormalizedStep):
                buildBar += "#"
            for i in range(remaingBuildNormalizedStep):
                buildBar += "-"
            buildBar += "] "

            print("PDF building " + buildBar + " (" + str(buildStep) + "/" + str(buildStepCount) + ")")
        
        firstImage = imageList[0]
        otherImages = imageList[1:]

        firstImage.save(pdfLocation , save_all=True, append_images=otherImages)
        currrentOptionIndex = 0
        
    elif options[currrentOptionIndex] == "clean":
        for manga in os.listdir(downloadLocation):
            if os.path.exists(downloadLocation + manga + extractSuffix):
                shutil.rmtree(downloadLocation + manga + extractSuffix)
            if os.path.exists(downloadLocation + manga + pagesSuffix):
                shutil.rmtree(downloadLocation + manga + pagesSuffix)
        currrentOptionIndex = 0



quit()







