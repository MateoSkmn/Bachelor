import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { RecordListItem } from '../interfaces/record-list-item.interface';
import { ModelListItem } from '../interfaces/model-list-item.interface';
import { Response } from '../interfaces/response.interface';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private BASE_URL: string = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  /**
   * 
   * @returns List of records stored in the BE
   */
  getRecords(): Observable<RecordListItem[]> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.get<RecordListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  /**
   * 
   * @returns List of models stored in the BEs
   */
  getModels(): Observable<ModelListItem[]> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.get<ModelListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  /**
   * 
   * @param file_name Record name
   * @param id Index of the instance
   * @returns LIME explanation values as well as information about the instance
   */
  getLime(file_name: string, id: number): Observable<any> {
    const url = `${this.BASE_URL}/data/record/${file_name}/${id}/lime`;
    return this.http.get<any>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  /**
   * 
   * @param body File to be uploaded
   * @returns Success information
   */
  postRecord(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  /**
   * 
   * @param body File to be uploaded
   * @returns Success information
   */
  postModel(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  /**
   * 
   * @param file_name Record name
   * @param body [index, understandable, prediction]
   * @returns Success information
   */
  postEvaluation(file_name: string, body: number[]): Observable<any> {
    const url = `${this.BASE_URL}/data/user-info/evaluation/${file_name}`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  /**
   * 
   * @param body [record name, model name]
   * @returns Success information
   */
  postConnection(body: string[]): Observable<any> {
    const url = `${this.BASE_URL}/data/user-info/connection`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  /**
   * 
   * @param file_name Record name
   * @returns Success information
   */
  deleteRecord(file_name: string): Observable<Response> {
    const url = `${this.BASE_URL}/data/record/${file_name}`;
    return this.http.delete<Response>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  /**
   * 
   * @param file_name Model name
   * @returns Success information
   */
  deleteModel(file_name: string): Observable<Response> {
    const url = `${this.BASE_URL}/data/model/${file_name}`;
    return this.http.delete<Response>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }
}
