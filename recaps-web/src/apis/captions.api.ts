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

export function updateCaption(params: any) {
  return unauthorizedRequest.put(`/UpdateCaption`, params);
}

export function deleteCaption(params: string) {
  return unauthorizedRequest.delete(`/removeCaption?idCaption=${params}`);
}
