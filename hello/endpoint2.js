import request from 'Services/request';
import hours from 'Constants/hours';
import countries from 'Constants/countries';
import PROXY_URL from 'Constants/proxy'
import axios from 'axios';
const DEFAULT_HOURS = hours[0];
const COUNTRIES = countries;

const DEFAULT_CLIENT = 'sanisidro';

const getCampaings = async ({client = DEFAULT_CLIENT}) => {
  const [data] = await request.rawGet(
      `/api/v1/bg/bg-input-name/${client}`,
      PROXY_URL,
  );
  if (!data) {
    return [[], null];
  }

  return [(data.data || []).map(c => ({
    label: c.Nombre_campaña,
    value: c.Input_Name,
    project_id: c.Id,
  })), null];
}

const getSharedCountByUrl = async ({id}) => {
  if (!id) {
    return [];
  }
  const data = await request.rawGet(
      `api/v1/bg/bg-documents-sharedcount/${id}`,
      PROXY_URL
  );
  if (!data) {
    return [[], null];
  }else{
    return data;
  }
};
const getNotes = async ({campaign, hour = DEFAULT_HOURS, keywordFilter, countryFilter}) => {
  if (!campaign) {
    return [];
  }
  if (keywordFilter) {
    if (campaign.value==="all"){
      if (countryFilter && countryFilter.value == "0") {
        return await request.rawGet(
            `/api/v1/bg/bg-documents-7-days-all-by-client-and-keywords/${campaign.project_id}/${hour.value}/${keywordFilter}`,
            PROXY_URL,
        );
      }else{
        return await request.rawGet(
            `/api/v1/bg/bg-documents-7-days-all-by-client-and-keyword-and-country/${campaign.project_id}/${hour.value}/${keywordFilter}/${countryFilter.value.toLowerCase()}`,
            PROXY_URL,
        );
      }
    }else{
      if (countryFilter && countryFilter.value == "0") {
        return await request.rawGet(
            `/api/v1/bg/bg-documents-7-days-by-keywords/${campaign.value}/${hour.value}/${keywordFilter}`,
            PROXY_URL,
        );
      }else{
        return await request.rawGet(
            `/api/v1/bg/bg-documents-7-days-by-keywords-and-country/${campaign.value}/${hour.value}/${keywordFilter}/${countryFilter.value.toLowerCase()}`,
            PROXY_URL,
        );
      }
    }

  }
  if (campaign.value==="all" && countryFilter) {

    if (countryFilter && countryFilter.value == "0") {
      var dato =  [];
      var keywords = [];
      var keywordsObject = [];
      var arr = [];
      var arrayReturn = [];

      //async function rawGetApi() {
      dato = request.rawGet(
          `/api/v1/bg/bg-documents-7-days-all-by-client/${campaign.project_id}/${hour.value}`,
          PROXY_URL,
      );
      
      return Promise.all([dato]).then(values => {
        console.log(values);
        return values;
        var myJsonString = JSON.stringify(values[0][0].data);
        var datoPost = axios.post('http://127.0.0.1:8000/keywordextract/', 
          myJsonString); 
        arrayReturn = values;
        console.log(arrayReturn);
        console.log(arrayReturn[0][0]);
        return values;
        return Promise.all([datoPost]).then(values => {
            console.log(values);
            //console.log(values[0]['config']['data']);JSON.parse(
            //var myJsonString = JSON.parse(values[0]['data']);
            var myJsonString = values[0]['data'];
            //myJsonString = "'" + myJsonString + "'";
            //myJsonString = JSON.stringify(myJsonString);
            myJsonString = myJsonString.replace(/"/g, '');
            myJsonString = myJsonString.replace(/'/g, '"');
            console.log(myJsonString);
            myJsonString = JSON.parse(myJsonString);
            console.log(myJsonString);
            //arrayReturn[0][0].data = myJsonString
            return arrayReturn;
          
        });
      });


    } else {
      return await request.rawGet(
          `/api/v1/bg/bg-documents-7-days-all-by-client-and-country/${campaign.project_id}/${hour.value}/${countryFilter.value.toLowerCase()}`,
          PROXY_URL,
      );
    }
  }

  if (countryFilter && countryFilter.value != "0") {
    return await request.rawGet(
        `/api/v1/bg/bg-documents-7-days-by-country/${campaign.value}/${hour.value}/${countryFilter.value.toLowerCase()}`,
        PROXY_URL,
    );
  }
  const data = await request.rawGet(
      `/api/v1/bg/bg-documents-7-days/${campaign.value}/${hour.value}`,
      PROXY_URL,
  );
  if (!data) {
    return [[], null];
  }else{
    return data;
  }
};
const getFeaturedNotes = ({campaign, hour = DEFAULT_HOURS, country}) => {
  if (country) {
    return request.rawGet(
        // `/cache/top_articles?project_id=${country}&time_interval=${hour.value}`,
        `/countryNews.php?project_id=${country}&time_interval=${hour.value}`,
        PROXY_URL
    );
  }

  if (!campaign) {
    return [];
  }
  if (campaign.label==="Todas") {
    return request.get(
        `/cache/campaign/mult/clipping/300/0/q.json?campaigns=${campaign.value}&section=All&recent=${hour.value}&no_cache=false&ttl2=1440`
        //`/cache/campaign/summary/300/0/q.json?campaign=${campaign.value}&section=All&recent=${hour.value}`
    );
  }
  return [];
}

const getTopics = ({campaign, hour = DEFAULT_HOURS, country, keywordFilter}) => {
  if (country) {
    const section = keywordFilter ? keywordFilter : "All";
    return request.rawGet(
        `/countryTopics.php?country=${country}&section=${section}`,
        PROXY_URL
        // `http://illuminati-web.7puentes.com/cache/home/summary/10/0/q.json?proj=${country}&section=${section}`
    );
  }

  if (!campaign) {
    return [];
  }
  if (campaign.label==="Todas") {
    return request.get(
        `cache/campaign/mult/summary/300/0/q.json?campaigns=${campaign.value}&section=All&recent=${hour.value}`
        //`/cache/campaign/summary/300/0/q.json?campaign=${campaign.value}&section=All&recent=${hour.value}`
    );
  }
  return [];
}

const getComments = ({groupId}) => {
  if (!groupId) {
    return [];
  }

  return request.rawGet(
      `/online/groups/${groupId}/comments.json`,
      'http://illuminati-web.7puentes.com/',
  );
}


const getCampaignKeywords = ({campaign}) => {
  if (!campaign) {
    return [];
  }

  return [];
};

const getCountries = async ({client = DEFAULT_CLIENT, countries = COUNTRIES}) => {
  const [data] = await request.rawGet(
      `/api/v1/bg/bg-countries-by-client/${client}`,
      PROXY_URL,
  );
  if (!data) {
    return [[], null];
  }
  let countriesRet = [];
  for (let val of data.data) {
    for(var i=0;i<countries.length;i++){
      if(countries[i].value.toLowerCase() == val.Country.toLowerCase()){
        countriesRet.push(countries[i]);
      }
    }
  }
  return [countriesRet];
}


const getWordcloud = ({groupId}) => request.rawGet(
    `/online/groups/${groupId}/wordcloud.json`,
    'http://illuminati-web.7puentes.com/',
);

const featuredThemeWordcloud = ({groupId}) => request.rawGet(
    `/cache/groups/${groupId}/articles.json`,
    'http://illuminati-web.7puentes.com/',
);

const getEvolution = ({ client, country }) => request.rawGet(
    `/cache/hits/section.json?proyecto=${country || client }&rango=dia`,
    'http://illuminati-web.7puentes.com/',
);

const getMostUsedWords = ({ country, campaign }) => {
  const destination = country
      ? `${PROXY_URL}/forcegraphWordsCountry.php?country=${country}`
      : `${PROXY_URL}/forcegraphWordsCampaign.php?campaign=${campaign.value}`;

  return request.rawGet(
      destination
  );
}

const loginUser = ({ user = DEFAULT_CLIENT }) => {
  return request.rawPost(`http://52.41.35.190/users/${user}`).post(`http://52.41.35.190/users/${user}`);
}

export const ENDPOINTS = {
  featuredNotes: getFeaturedNotes,
  notes: getNotes,
  sharedCount: getSharedCountByUrl,
  topics: getTopics,
  wordcloud: getWordcloud,
  login: loginUser,
  campaigns: getCampaings,
  comments: getComments,
  countries: getCountries,
  campaignKeywords: getCampaignKeywords,
  evolution: getEvolution,
  mostUsedWords: getMostUsedWords,
  featuredThemeWordcloud,
};
