import { EventEmitter, Injectable } from "@angular/core";
import { Response } from "../interfaces/response.interface";

@Injectable({
    providedIn: 'root'
})
export class ErrorService {
    errorEvent: EventEmitter<Response> = new EventEmitter<Response>();

    /**
     * Used to show errors globally
     * @param error Any type of error
     */
    triggerError(error: any) {
        this.errorEvent.emit(error);
    }
}