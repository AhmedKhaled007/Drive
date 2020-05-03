function doGet(e) {
  var folders = DriveApp.getFoldersByName('Apple Trailers')
  if (folders.hasNext()){
    apple_folder = folders.next()
  }
  else {
    apple_folder = DriveApp.createFolder('Apple Trailers')
  }
  var blob = UrlFetchApp.fetch(e.parameters.url).getBlob();
  var url = apple_folder.createFile(blob).getUrl();
  return ContentService.createTextOutput("file uploaded successfully, linl " + url);
}
