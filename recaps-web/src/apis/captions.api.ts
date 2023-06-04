import authorizedRequest from "@/config/authorizedRequest";
import unauthorizedRequest from "@/config/unauthorizedRequest";

interface NewCaptionBody {
  content: string;
  idUser: number;
  trangThai: boolean;
  tags?: string[];
  favourite?: boolean;
  userId?: string;
}

interface NewCaptionBody {
  Content: string;
  IDCaption: number;
  TrangThai: boolean;
  IDTag: string;
  IDUser: string;
}
export function getListCaptions() {
  return unauthorizedRequest.get(`/caption/get_all_caption`);
}

export function addNewCaption(body: NewCaptionBody) {
  return authorizedRequest.post(`/caption/add_caption`, body);
}

export function updateContentCaption(body: any) {
  return unauthorizedRequest.post(`/UpdateCaption`, body);
}

export function updateEmotionCaption(body: any) {
  return unauthorizedRequest.post(`/UpdateCaption`, body);
}

export function updateTagCaption(body: any) {
  return unauthorizedRequest.post(`/UpdateCaption`, body);
}

export function deleteCaption(body: any) {
  return unauthorizedRequest.post(`caption/delete_caption`, body);
}

export function getListCaptionFavourite() {
  return authorizedRequest.get(`/caption/get_caption_favorite`);
}
