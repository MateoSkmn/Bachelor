import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';
import { StyledButtonComponent } from '../../global/components/styled-button/styled-button.component';
import { Subscription } from 'rxjs';
import { ApiService } from '../../global/service/api.service';
import { ErrorService } from '../../global/service/error.service';
import { ModelListItem } from '../../global/interfaces/model-list-item.interface';
import { ModelTableRowComponent } from './model-table-row/model-table-row.component';

@Component({
  selector: 'app-model',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent, ModelTableRowComponent],
  templateUrl: './model.component.html',
  styleUrl: './model.component.scss'
})
export class ModelComponent implements OnInit, OnDestroy {

  @ViewChild('fileInput') fileInput!: ElementRef;

  private recordListSubscription!: Subscription;
  private uploadSubscription!: Subscription;

  modelList: ModelListItem[] = [];

  constructor(private apiService: ApiService, private errorService: ErrorService) {}

  ngOnInit(): void {
    this.recordListSubscription = this.apiService.getModels().subscribe({
      next: (response) => {
        this.modelList = response;
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }

  ngOnDestroy(): void {
    if (this.recordListSubscription) {
      this.recordListSubscription.unsubscribe();
    }
    if (this.uploadSubscription) {
      this.uploadSubscription.unsubscribe();
    }
  }

  uploadFile(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    this.uploadSubscription = this.apiService.postModel(formData).subscribe({
      next: (response) => {
        window.location.reload();
      },
      error: (error) => {
        this.errorService.triggerError(error);
      }
    });
  }
}
