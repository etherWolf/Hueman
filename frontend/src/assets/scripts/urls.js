let serverBaseURL = 'http://localhost:5000';

// The names may be a little confusing. So, read the comments.

export const serverURLs = {
  'SEARCH': serverBaseURL + '/search', // used to 'perform' the actual search. params are passed in a query string.
  'FETCH-SEARCH-DATA': serverBaseURL + '/getsearchdata', // used to get the search form data to load into the fields.
  'INITIATE-UPLOAD-SESSION': serverBaseURL + '/initiateuploadsession', // to begin a new 'session' of uploads (see backend code for more details)
  'UPLOAD': serverBaseURL + '/upload', // to upload an image
  'GET-IMAGE': serverBaseURL + '/uploads/',
  'DELETE-IMAGE': serverBaseURL + '/delete/',
  'POST-DATA': serverBaseURL + '/postdata',
};
