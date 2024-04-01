export namespace LiveChatMessages {
  export interface LiveChatMessageListResponse {
    kind: string;
    etag: string;
    pollingIntervalMillis: number;
    pageInfo: PageInfo;
    nextPageToken: string;
    items: LiveChatMessage[];
  }

  interface PageInfo {
    totalResults: number;
    resultsPerPage: number;
  }

  export interface LiveChatMessage {
    kind: string;
    etag: string;
    id: string;
    snippet: LiveChatMessageSnippet;
    authorDetails: LiveChatMessageAuthorDetails;
  }

  interface LiveChatMessageAuthorDetails{
    channelId: string;
    channelUrl: string;
    displayName: string;
    profileImageUrl: string;
    isVerified: boolean;
    isChatOwner: boolean;
    isChatSponsor: boolean;
    isChatModerator: boolean;
  }

  interface LiveChatMessageSnippet {
    type: string;
    liveChatId: string;
    authorChannelId: string;
    publishedAt: string;
    hasDisplayContent: boolean;
    displayMessage: string;
    textMessageDetails: TextMessageDetails;
  }

  interface TextMessageDetails {
    messageText: string;
  }
}

export namespace LiveBroadcasts {
  export interface LiveBroadcastListResponse {
    kind: string;
    etag: string;
    pageInfo: PageInfo;
    items: LiveBroadcast[];
  }

  interface PageInfo {
    totalResults: number;
    resultsPerPage: number;
  }

  interface LiveBroadcast {
    kind: string;
    etag: string;
    id: string;
    snippet: LiveBroadcastSnippet;
  }

  interface LiveBroadcastSnippet {
    publishedAt: string;
    channelId: string;
    title: string;
    description: string;
    thumbnails: Thumbnails;
    scheduledStartTime: string;
    actualStartTime: string;
    isDefaultBroadcast: boolean;
    liveChatId: string;
  }

  interface Thumbnails {
    default: Thumbnail;
    medium: Thumbnail;
    high: Thumbnail;
    standard: Thumbnail;
    maxres: Thumbnail;
  }

  interface Thumbnail {
    url: string;
    width: number;
    height: number;
  }
}


export interface Token{
  access_token:string|null
  expires_in:number|null
  expired_time:Date|undefined
}