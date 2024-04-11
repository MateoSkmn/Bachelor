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

  // TODO: Weitere & Refactoring

  getRecords(): Observable<RecordListItem[]> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.get<RecordListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  getModels(): Observable<ModelListItem[]> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.get<ModelListItem[]>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  getLime(file_name: string, id: number): Observable<any> {
    const url = `${this.BASE_URL}/data/record/${file_name}/${id}/lime`;
    return this.http.get<any>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  postRecord(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/record`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  postModel(body: FormData): Observable<any> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  postEvaluation(file_name: string, body: number[]): Observable<any> {
    const url = `${this.BASE_URL}/data/user-info/evaluation/${file_name}`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  postConnection(body: string[]): Observable<any> {
    const url = `${this.BASE_URL}/data/user-info/connection`;
    return this.http.post<any>(url, body).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  deleteRecord(file_name: string): Observable<Response> {
    const url = `${this.BASE_URL}/data/record/${file_name}`;
    return this.http.delete<Response>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }

  deleteModel(): Observable<Response> {
    const url = `${this.BASE_URL}/data/model`;
    return this.http.delete<Response>(url).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    )
  }
}
